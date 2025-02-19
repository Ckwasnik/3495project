const express = require('express');
const { MongoClient } = require('mongodb');

const app = express();
const url = "mongodb://mongo:27017/";
const dbName = "analytics_db";

app.get("/results", async (req, res) => {
    const client = new MongoClient(url);
    await client.connect();
    const db = client.db(dbName);
    const stats = await db.collection("stats").findOne({}, { sort: { _id: -1 } });

    res.json(stats);
    client.close();
});

app.listen(5003, () => console.log("Show Results running on port 5003"));
