const fromCurrency = document.getElementById("fromCurrency");
const toCurrency = document.getElementById("toCurrency");
const result = document.getElementById("result");
const historyList = document.getElementById("history");

const currencyList = ["USD", "INR", "EUR", "GBP", "JPY", "CAD"];
let conversionHistory = [];

function CurrencyDropping() {
    currencyList.forEach(curr => {
        fromCurrency.innerHTML += `<option value="${curr}">${curr}</option>`;
        toCurrency.innerHTML += `<option value="${curr}">${curr}</option>`;
    });
    fromCurrency.value = "USD";
    toCurrency.value = "INR";
}

async function convertingCurrency() {
    const amount = document.getElementById("amount").value;
    const from = fromCurrency.value;
    const to = toCurrency.value;

    if (!amount || amount <= 0) {
        result.textContent = "⚠️ Enter a valid amount!";
        return;
    }

    try {
        const res = await fetch(`https://api.exchangerate-api.com/v4/latest/${from}`);
        const data = await res.json();
        const rate = data.rates[to];
        const converted = (amount * rate).toFixed(2);
        result.textContent = `Result: ${amount} ${from} = ${converted} ${to}`;
        logHistory(`${amount} ${from} = ${converted} ${to}`);
    } catch (err) {
        result.textContent = "❌ Error fetching data.";
    }
}

function logHistory(entry) {
    const timestamp = new Date().toLocaleTimeString();
    const fullEntry = `[${timestamp}] ${entry}`;
    conversionHistory.unshift(fullEntry);
    if (conversionHistory.length > 5) conversionHistory.pop();
    updatingHistory();
}

function updatingHistory() {
    historyList.innerHTML = "";
    conversionHistory.forEach(item => {
        const li = document.createElement("li");
        li.textContent = item;
        historyList.appendChild(li);
    });
}

function ThemeChange() {
    document.getElementById("themeContainer").classList.toggle("dark-mode");
}

CurrencyDropping();
