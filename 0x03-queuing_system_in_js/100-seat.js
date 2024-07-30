import express from 'express';
import { promisify } from 'util';
import { createQueue } from 'kue';
import { createClient } from 'redis';

const app = express();
const redisClient = createClient({ name: 'reserve_seat' });
const rsrvQueue = createQueue();
const defaultSeatCount = 50;
let reservationEnabled = false;
const port = 1245;

const reserveSeat = async (number) => {
  return promisify(redisClient.SET).bind(redisClient)('available_seats', number);
};

const getCurrentAvailableSeats = async () => {
  return promisify(redisClient.GET).bind(redisClient)('available_seats');
};

app.get('/available_seats', (_, res) => {
  getCurrentAvailableSeats()
    .then((numberOfAvailableSeats) => {
      res.json({ numberOfAvailableSeats });
    });
});

app.get('/reserve_seat', (_req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }
  try {
    const rsrvJob = rsrvQueue.create('reserve_seat');
    rsrvJob.on('failed', (err) => {
      console.log('Seat rreservation job', rsrvJob.id, 'failed:', err.message || err.toString());
    });
    rsrvJob.on('complete', () => {
      console.log('Seat reservation job', rsrvJob.id, 'completed');
    });
    rsrvJob.save();
    res.json({ status: 'Reservation in process' });
  } catch (error) {
    console.error('Reservation failed:', error);
    res.json({ status: 'Reservation failed' });
  }
});

app.get('/process', (_req, res) => {
  res.json({ status: 'Queue processing' });
  rsrvQueue.process('reserve_seat', (_job, done) => {
    getCurrentAvailableSeats()
      .then((currSeatCount) => Number.parseInt(currSeatCount || 0))
      .then((availableSeats) => {
        reservationEnabled = availableSeats <= 1 ? false : reservationEnabled;
        if (availableSeats >= 1) {
          reserveSeat(availableSeats - 1)
            .then(() => done());
        } else {
          done(new Error('Not enough seats available'));
        }
      });
  });
});

const initializeSeats = async (seatsToInitialize) => {
  return promisify(redisClient.SET)
    .bind(redisClient)('available_seats', Number.parseInt(seatsToInitialize));
};

app.listen(port, () => {
  initializeSeats(process.env.defaultSeatCount || defaultSeatCount)
    .then(() => {
      reservationEnabled = true;
      console.log(`API available on localhost port ${port}`);
    });
});

export default app;
