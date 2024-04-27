require("./js_hook.js")
const {
    EventEmitter
} = require('events');
const Websocket = require("ws")
const express = require("express");
const {
    Worker
} = require("worker_threads");
const app = express();
let tasks = {}
let tasksarr = []
let ready = []
app.use(express.json());

const start_worker = () => {
    for (let i = 0; i < 1; i++) {
        let worker = new Worker("./get_captcha.js")
        worker.on("message", (data) => {
            console.log("Data recv")
            if (data.event == "new_data") {
                let idx = Math.floor(Math.random() * tasksarr.length)
                if (idx == 0) {
                    ready.push(data.value)
                }
                let task = tasksarr[idx]
                tasks[task] = {
                    status: "COMPLETE",
                    value: data.value
                }
                tasksarr.splice(idx)
            }
        })
    }
}

class SocketListener extends EventEmitter {
    constructor() {
        super();

        this.server = new Websocket.Server({
            port: 1234
        });
        console.log("WS UP")
        this.client = undefined;
        this.vals = {}
    }

    async start() {
        this.server.on("connection", (socket) => {
            this.client = socket;
            this.client.on('message', (data) => this.emit('resolve', data));

            this.emit('ready');
            console.log(`[-] New browser connected.`);
        });
    }

    send(data) {
        this.client.send(JSON.stringify(data));
    }
}

const Client = new SocketListener();

app.get("/submit_cap", async (req, res) => {
    let taskId = Math.floor(Math.random() * 1000000000000000000);
    tasksarr.push(taskId)
    tasks[taskId] = {
        status: "PENDING",
        value: "NOT_GIVEN",
        array_index: tasksarr.length - 1
    }
    return res.status(200).send({
        status: "SUCCESS",
        taskId: taskId
    })
})

app.get("/submit_cap/resp/:taskId", async (req, res) => {
    let taskId = req.params.taskId;
    let task = tasks[taskId]
    if (task["status"] == "PENDING" && ready.length !== 0) {
        let idx = Math.floor(Math.random() * ready.length)
        task["value"] = ready[idx];
        task["status"] == "COMPLETE";
        ready.splice(idx);
        tasksarr.splice(task["array_index"]);
    }
    return res.status(200).send({
        task
    })
})



app.get("/get_captcha", async (req, res) => {
    let taskId = Math.floor(Math.random() * 1000000000000000000);
    tasksarr.push(taskId)
    tasks[taskId] = {
        status: "PENDING",
        value: "NOT_GIVEN",
        array_index: tasksarr.length - 1
    }
    return res.status(200).send({
        status: "SUCCESS",
        taskId: taskId
    })
})

app.get("/get_captcha/resp/:taskId", async (req, res) => {
    let taskId = req.params.taskId;
    let task = tasks[taskId]
    if (task["status"] == "PENDING" && ready.length !== 0) {
        let idx = Math.floor(Math.random() * ready.length)
        task["value"] = ready[idx];
        task["status"] == "COMPLETE";
        ready.splice(idx);
        tasksarr.splice(task["array_index"]);
    }
    return res.status(200).send({
        task
    })
})


app.post("/getn", async (req, res) => {
    let reqval = req.body.task;
    console.log(reqval)
    await Client.send({
        solve: reqval
    });

    Client.once('resolve', async (data) => {
        res.send(JSON.parse(data).token);
    });
})




app.listen(5435, async () => {
    console.log("Listening on 5435")
    await Client.start()
})
start_worker()