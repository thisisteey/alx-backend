import express from 'express';
import { promisify } from 'util';
import { createClient } from 'redis';

const listProducts = [
  {
    itemId: 1,
    itemName: 'Suitcase 250',
    price: 50,
    initialAvailableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: 'Suitcase 450',
    price: 100,
    initialAvailableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: 'Suitcase 650',
    price: 350,
    initialAvailableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: 'Suitcase 1050',
    price: 550,
    initialAvailableQuantity: 5,
  },
];

const getItemById = (id) => {
  const prodItem = listProducts.find(obj => obj.itemId === id);

  if (prodItem) {
    return Object.fromEntries(Object.entries(prodItem));
  }
};

const app = express();
const redisClient = createClient();
const port = 1245;

const reserveStockById = async (itemId, stock) => promisify(redisClient.SET).bind(redisClient)(`item.${itemId}`, stock);

const getCurrentReservedStockById = async (itemId) => promisify(redisClient.GET).bind(redisClient)(`item.${itemId}`);

app.get('/list_products', (_, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId(\\d+)', (req, res) => {
  const itemId = Number.parseInt(req.params.itemId);
  const prodItem = getItemById(Number.parseInt(itemId));

  if (!prodItem) {
    res.json({ status: 'Product not found' });
    return;
  }
  getCurrentReservedStockById(itemId)
    .then((rsvdStockVal) => Number.parseInt(rsvdStockVal || 0))
    .then((prsdRsvdStock) => {
      prodItem.currentQuantity = prodItem.initialAvailableQuantity - prsdRsvdStock;
      res.json(prodItem);
    });
});

app.get('/reserve_product/:itemId', (req, res) => {
  const itemId = Number.parseInt(req.params.itemId);
  const prodItem = getItemById(Number.parseInt(itemId));

  if (!prodItem) {
    res.json({ status: 'Product not found' });
    return;
  }
  getCurrentReservedStockById(itemId)
    .then((rsvdStockVal) => Number.parseInt(rsvdStockVal || 0))
    .then((prsdRsvdStock) => {
      if (prsdRsvdStock >= prodItem.initialAvailableQuantity) {
        res.json({ status: 'Not enough stock available', itemId });
        return;
      }
      reserveStockById(itemId, prsdRsvdStock + 1)
        .then(() => {
          res.json({ status: 'Reservation confirmed', itemId });
        });
    });
});

const initializeStock = () => Promise.all(
  listProducts.map(
    (item) => promisify(redisClient.SET).bind(redisClient)(`item.${item.itemId}`, 0),
  ),
);

app.listen(port, () => {
  initializeStock()
    .then(() => {
      console.log(`API available on localhost port ${port}`);
    });
});

export default app;
