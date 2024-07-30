import { createQueue } from 'kue';

const blacklistedPhoneNumbers = ['4153518780', '4153518781'];
const notifQueue = createQueue();

const sendNotification = (phoneNumber, message, job, done) => {
  const totalAtms = 2; let pendingAtms = 2;
  const notifInterval = setInterval(() => {
    if (totalAtms - pendingAtms <= totalAtms / 2) {
      job.progress(totalAtms - pendingAtms, totalAtms);
    }
    if (blacklistedPhoneNumbers.includes(phoneNumber)) {
      done(new Error(`Phone number ${phoneNumber} is blacklisted`));
      clearInterval(notifInterval);
      return;
    }
    if (totalAtms === pendingAtms) {
      console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
    }
    pendingAtms -= 1;
    if (pendingAtms === 0) {
      done();
      clearInterval(notifInterval);
    }
  }, 1000);
};

notifQueue.process('push_notification_code_2', 2, (notifJob, done) => {
  sendNotification(notifJob.data.phoneNumber, notifJob.data.message, notifJob, done);
});
