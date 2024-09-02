let clickTime = null;
let isClicked = false;
const dataContainer = [];

export function handleTracking(button) {
    const now = new Date();
    if (!isClicked) {
        // Record click time
        clickTime = now.toISOString();
        button.classList.add('click');
        isClicked = true;
    } else {
        // Record unclick time and save data
        dataContainer.push({ clickTime, unclickTime: now.toISOString() });
        button.classList.remove('click');
        isClicked = false;
        clickTime = null;
        console.log(dataContainer)
    }
}

export async function sendData() {
    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ dataContainer })
        });
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        const name = new Date()
        link.setAttribute('download', `${name.toISOString()}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error downloading CSV:', error);
    }
}