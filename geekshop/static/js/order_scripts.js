window.onload = function () {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_array = [];
    let price_array = [];

    let TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    console.log(order_total_quantity, order_total_cost);
    for (let i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));
        quantity_array[i] = _quantity;
        if (_price) {
            price_array[i] = _price;
        } else {
            price_array[i] = 0;
        }
    }

    if (!order_total_quantity) {
        orderSummaryRecalc();
    }

    function orderSummaryRecalc() {
        order_total_quantity = 0;
        order_total_cost = 0;
        for (let i = 0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_array[i];
            order_total_cost += quantity_array[i] * price_array[i];
        }
        $('.order_total_quantity').html(order_total_quantity.toString());
        $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    }

    $('.order_form').on('click', 'input[type="number"]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_array[orderitem_num]) {
            console.log(orderitem_num)
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_array[orderitem_num];
            quantity_array[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_array[orderitem_num], delta_quantity);
        }
    });

    $('.order_form').on('click', 'input[type="checkbox"]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            delta_quantity = -quantity_array[orderitem_num];
        } else {
            delta_quantity = quantity_array[orderitem_num];
        }
        orderSummaryUpdate(price_array[orderitem_num], delta_quantity);
    });


    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;

        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_cost').html(order_total_cost.toString());
        $('.order_total_quantity').html(order_total_quantity.toString());
    }

    $('.formset_row').formset({
        addText: 'добавить товар',
        deleteText: 'удалить',
        prefix: 'orderitems',
        removed: deleteOrderItem
    });

    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type=number]').name;
        let orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-DELETE', ''));
        delta_quantity = -quantity_array[orderitem_num];
        orderSummaryUpdate(price_array[orderitem_num], delta_quantity);
    }

    $('.order_form').on('change', 'select', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        let orderitem_product_pk = target.options[target.selectedIndex].value;

        if (orderitem_product_pk) {
            $.ajax({
                url: "/order/product/" + orderitem_product_pk + "/price/",
                success: function (data) {
                    if (data.price) {
                        price_array[orderitem_num] = parseFloat(data.price);
                        if (isNaN(quantity_array[orderitem_num])) {
                            quantity_array[orderitem_num] = 0;
                        }
                        let price_html = '<span>' + data.price.toString().replace('.', ',') + '</span> руб';
                        let current_tr = $('.order_form table').find('tr:eq(' + (orderitem_num + 1) + ')');
                        current_tr.find('td:eq(2)').html(price_html);

                        if (isNaN(current_tr.find('input[type="number"]'))) {
                            current_tr.find('input[type="number"]').val(0);
                        }
                        orderSummaryRecalc();
                    }
                },
            });
        }
    });
}