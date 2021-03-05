var updateBtns = document.getElementsByClassName('update-cart')
for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;

        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOreder(productId, action)
        }
    })
}

// Se activa cuando la pagina carga
document.addEventListener("DOMContentLoaded", getOrder(undefined));

// Consulta la orden del usuario y trae los productos
function getOrder(coupon) {
    $.ajax({
        type: 'GET',
        url: `/get_checkout_items/${orderId}`,
        contentType: 'application/json; charset=utf-8',
        success: function (res) {
            console.log('res ', res);
            var items = res.items;
            var quantity = items.length;
            var delivery = 7000;
            var subTotal = 0;
            var sum = items.forEach((i) => {
                data = JSON.parse(i)
                subTotal += parseInt(data.price);
            });
            console.log('subTotal ', subTotal);
            if (coupon && coupon > 0) {
                var total_c = 0;
                var coupon_value = coupon / 100;
                var discount = coupon_value * subTotal;
                var sub = subTotal - discount;
                total_c = sub + delivery;
                console.log('total if ', total_c);

                // Aqui viene el codigo que pintara en html la tabla del resumen de la compra con cupon
                const originalTable = document.querySelector(".original-table"); // Tabla original de DJANGO
                const tablecuponOutput = document.querySelector(".table-cupon-output");
                const tbody1 = document.querySelector(".table-cupon1");
                const tbody2 = document.querySelector(".table-cupon2");

                console.log("data xxxx con cupon", data);
                originalTable.style.display = "none"; // Tabla original de DJANGO
                tablecuponOutput.style.display = "block";
    
                items.forEach((items) => {
                    tbody1.innerHTML += `
                    <tr>
                        <td>${items.name}}</td>
                        <td>${items.presenta}}</td>
                        <td>${items.quantity}}</td>
                        <td>$ ${items.price}}</td>
                        <td>$ ${items.total_c}}</td>
                    </tr>
                    `
                });
                tbody2.innerHTML += `
                    <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td><h6>Sub Total del Canasto: </h6></td>
                        <td><strong>${subTotal}</strong></td>

                    </tr>
                    <tr>
                        <td></td>
                        <td><h6>Cupon: ${coupon_value} % </h6></td>
                        <td><strong>{{coupon}}</strong></td>
                        <td><h6>Descuento del Cupon: </h6></td>
                        <td><strong>${sub}</strong></td>
                    </tr>
                    <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>Domicilio</td>
                        <td>$ ${delivery}</td>
                    </tr>
                    <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td><h6>Total del Canasto: </h6></td>
                        <td><strong>${total_c}</strong></td>
                    </tr>
                    `

            } else {
                var total = subTotal + delivery;
                console.log('total else ', total);

                // Aqui viene el codigo que pintara en html la tabla del resumen de la compra sin cupon
                const originalTable = document.querySelector(".original-table"); // Tabla original de DJANGO
                const tablecuponOutput = document.querySelector(".table-cupon-output");
                const tbody1 = document.querySelector(".table-cupon1");
                const tbody2 = document.querySelector(".table-cupon2");

                console.log("data xxxx sin cupon", data);
                originalTable.style.display = "none"; // Tabla original de DJANGO
                tablecuponOutput.style.display = "block";
                
                for (i=0; i<data.length; i++){
                    tbody1.innerHTML += `
                    <tr>
                        <td>${data[i].name}}</td>
                        <td>${data[i].presenta}}</td>
                        <td>${data[i].quantity}}</td>
                        <td>$ ${data[i].price}}</td>
                        <td>$ ${data[i].total_c}}</td>
                    </tr>
                    `
                }

                //data.forEach((item) => {
                //    tbody1.innerHTML += `
                //    <tr>
                //        <td>${item.name}}</td>
                 //       <td>${item.presenta}}</td>
                //        <td>${item.quantity}}</td>
                //        <td>$ ${item.price}}</td>
                //        <td>$ ${item.total_c}}</td>
                //    </tr>
                //    `
                //});

                tbody2.innerHTML += `
                    <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td><h6>Sub Total del Canasto: </h6></td>
                        <td><strong>${subTotal}</strong></td>

                    </tr>
                    <tr>
                        <td></td>
                        <td><h6>Cupon: </h6></td>
                        <td><strong>{{coupon}}</strong></td>
                        <td><h6>Descuento del Cupon: </h6></td>
                        <td><strong></strong></td>
                    </tr>
                    <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>Domicilio</td>
                        <td>$ ${delivery}</td>
                    </tr>
                    <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td><h6>Total del Canasto: </h6></td>
                        <td><strong>${total}</strong></td>
                    </tr>
                `
            }
        },
        error: function () {
            console.log("error");
        }
    });

}

$('#sendCoupon').click(function (e) {
    // Se envia a verificar el cupon
    e.preventDefault();
    checkCoupon();
});

function checkCoupon() {
    var data = document.getElementById('cupon');
    if (data.value) {
        $.ajax({
            type: 'GET',
            url: `/validate_cupon?coupon=${data.value}`,
            contentType: 'application/json; charset=utf-8',
            success: function (res) {
                var discount = res.discount;
                var value = document.getElementById('cupon-value')
                value.innerHTML = discount;
                var clear = document.getElementById('clearCoupon')
                clear.classList.remove("hidden");
                getOrder(discount);
            },
            error: function () {
                console.log("error");
                var element = document.getElementById('cupon-error');
                element.classList.remove("hidden");
                var interval = setTimeout(function(){
                    element.classList.add("hidden");
                    data.value = '';
                }, 3000);
            }
        });
    }
}

function ClearDiscount() {
    var value = document.getElementById('cupon-value')
    value.innerHTML = ''
    getOrder(undefined);
}


function addCookieItem(productId, action) {

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