import { handleTracking, sendData } from './functions.js';

const socket = io();

socket.on('status_update', async (data) => {
    console.log(data.started)
    if (!data.started) {
        await sendData();
        window.location.href = '/waiting';
    } 
});

document.getElementById('trackButton').onclick = function() {
    handleTracking(this);
};
