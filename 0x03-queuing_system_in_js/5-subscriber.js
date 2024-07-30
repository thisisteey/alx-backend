import { createClient } from 'redis';

const redisClient = createClient();
const EXIT_CMD = 'KILL_SERVER';

redisClient.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

redisClient.on('connect', () => {
  console.log('Redis client connected to the server');
});

redisClient.subscribe('holberton school channel');

redisClient.on('message', (_err, msg) => {
  console.log(msg);
  if (msg === EXIT_CMD) {
    redisClient.unsubscribe();
    redisClient.quit();
  }
});
