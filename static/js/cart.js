var updateBtns = document.getElementsByClassName('update-cart')
for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action

        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOreder(productId, action)
        }
    })
}


function addCookieItem(productId, action) {
    console.log('User is not Authenticated')

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }
            alert('Item se adiciono al canasto')
        } else {
            cart[productId]['quantity'] += 1
            alert('Item se adiciono al canasto')
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1
        alert('Item se removió del canasto')

        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId];
            alert('Item se removió del canasto')
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}


function updateUserOreder(productId, action) {
    var url = '/update_item/'
    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({ 'productId': productId, 'action': action }),
        })
        .then((response) => {
            return response.json()
        })
        .then((data) => {
            location.reload()
        })
}