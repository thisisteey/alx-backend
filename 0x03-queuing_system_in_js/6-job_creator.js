import { createQueue } from 'kue';

const notifQueue = createQueue({ name: 'push_notification_code' });
const notifJob = notifQueue.create('push_notification_code', {
  phoneNumber: '08424283190',
  message: 'This is the code to verify your account',
});

notifJob
  .on('enqueue', () => {
    console.log('Notification job created:', notifJob.id);
  })
  .on('complete', () => {
    console.log('Notification job completed');
  })
  .on('failed', () => {
    console.log('Notification job failed');
  });
notifJob.save();
