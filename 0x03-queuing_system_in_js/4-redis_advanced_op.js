import { createClient, print } from 'redis';

const redisClient = createClient();

redisClient.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

const setHashField = (hashKey, hashField, hashValue) => {
  redisClient.HSET(hashKey, hashField, hashValue, print);
};

const logHashFields = (hashKey) => {
  redisClient.HGETALL(hashKey, (_err, reply) => console.log(reply));
};

function main() {
  const schoolScores = {
    Portland: 50,
    Seattle: 80,
    'New York': 20,
    Bogota: 20,
    Cali: 40,
    Paris: 2,
  };
  for (const [field, value] of Object.entries(schoolScores)) {
    setHashField('HolbertonSchools', field, value);
  }
  logHashFields('HolbertonSchools');
}

redisClient.on('connect', () => {
  console.log('Redis client connected to the server');
  main();
});
