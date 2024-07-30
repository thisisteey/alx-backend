const createPushNotificationsJobs = (jobs, queue) => {
  if (!(jobs instanceof Array)) {
    throw new Error('Jobs is not an array');
  }
  for (const jobData of jobs) {
    const notifJob = queue.create('push_notification_code_3', jobData);

    notifJob
      .on('enqueue', () => {
        console.log('Notification job created:', notifJob.id);
      })
      .on('complete', () => {
        console.log('Notification job', notifJob.id, 'completed');
      })
      .on('failed', (err) => {
        console.log('Notification job', notifJob.id, 'failed:', err.message || err.toString());
      })
      .on('progress', (progress) => {
        console.log('Notification job', notifJob.id, `${progress}% complete`);
      });
    notifJob.save();
  }
};

export default createPushNotificationsJobs;
