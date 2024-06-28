setInterval(function() {
    var lineItems = JSON.parse(document.getElementById('transactionsprof_lineitems').dataset.lineitems);
    var total = updateTotal(lineItems);
    document.getElementById('transactionsprof_total').value = total;
}, 1000);  // Adjust the interval as needed