import { createQueue } from 'kue';

const notifQueue = createQueue();

const sendNotification = (phoneNumber, message) => {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
};

notifQueue.process('push_notification_code', (notifJob, done) => {
  sendNotification(notifJob.data.phoneNumber, notifJob.data.message);
  done();
});
