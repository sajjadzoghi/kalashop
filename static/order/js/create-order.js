if (typeof sessionStorage.items === 'undefined') {
    window.location.href = "/"
}

let items = JSON.parse(sessionStorage.items);
for (let item of items) {
    $('tbody').append(`<tr id="item${item.product}">
                <td id="item-image"><img alt="${item.name}" style="width: 5rem" src="${item.image}"></td>
                <td id="item-name">${item.name}</td>
                <td id="item-color">${item.color}</td>
                <td id="item-price">${item.price}</td>
                <td id="item-count">${item.quantity}</td>
                <td id="item-final_price">${Number(item.price) * Number(item.quantity)}</td>
                <td class="item-delete"><i onclick="remove_item('${item.product}')" style="font-size: x-large;cursor: pointer" class="fa fa-fw fa-trash"></i></td>
            </tr>`);
}
$('table').after(`<h5 id="table-total" class="text-dark mr-auto"> مبلغ کل سفارش : ${sessionStorage.total_price} تومان</h5>
<p>______________________________________________________________________________________________</p>`);

if (sessionStorage.coupon_amount) {
    $('#coupon-btn').prop('disabled', 'true');
    $('#coupon').prop('disabled', 'true');
    $('#table-total').hide();
    $('table').after(`<h5 class="tbl-after text-dark mr-auto"> مبلغ کل سفارش <small>(با احتساب تخفیف)</small>: ${sessionStorage.total_price_coupon} تومان</h5>`);
    $('table').after(`<h5 class="tbl-after text-secondary mr-auto"><small>اعمال کد تخفیف</small>: ${sessionStorage.coupon_amount} - تومان</h5>`);
    $('table').after(`<h5 class="tbl-after text-secondary mr-auto"> <small>مبلغ کل سفارش (بدون احتساب تخفیف)</small>: ${sessionStorage.total_price} تومان</h5>`);
    $('#coupon-form').prepend(`<p class="text-success">* ${sessionStorage.coupon_amount} تومان از مبلغ کل سفارش شما کسر شد.</p>`);
    $('#add-address-btn').css('margin-top', '12.2rem');
}

$('#coupon-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
    var $crf_token = $('#coupon-form [name="csrfmiddlewaretoken"]').attr('value');

    var form_data = {
        'coupon': $('#coupon').val(),
    };

    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        headers: {"X-CSRFToken": $crf_token},
        success: function (resp) {
            $('#coupon-form p').remove();
            let total_price = Number(sessionStorage.total_price);
            sessionStorage.coupon_code = resp.code;
            sessionStorage.coupon_amount = total_price * resp.amount / 100;
            $('#add-address-btn').css('margin-top', '12.2rem');
            $(form).prepend(`<p class="text-success">* ${sessionStorage.coupon_amount} تومان از مبلغ کل سفارش شما کسر شد.</p>`);
            sessionStorage.total_price_coupon = total_price - (sessionStorage.coupon_amount);
            $('#table-total').hide();
            $('table').after(`<h5 class="tbl-after text-dark mr-auto"> مبلغ کل سفارش <small>(با احتساب تخفیف)</small>: ${sessionStorage.total_price_coupon} تومان</h5>`);
            $('table').after(`<h5 class="tbl-after text-secondary mr-auto"><small>اعمال کد تخفیف</small>: ${sessionStorage.coupon_amount} - تومان</h5>`);
            $('table').after(`<h5 class="tbl-after text-secondary mr-auto"> <small>مبلغ کل سفارش (بدون احتساب تخفیف)</small>: ${sessionStorage.total_price} تومان</h5>`);
            $('#coupon-btn').prop('disabled', 'true');
            $('#coupon').prop('disabled', 'true');

        },
        error: function (data) {
            $('#coupon-form p').remove();
            let errors = JSON.parse(data.responseText);
            for (let error_item in errors) {
                $(form).prepend(`<p class="text-danger">*${errors[error_item][0]}</p>`);
            }
        }
    });

});


$('#add-address-form').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');
    var $crf_token = $('#add-address-form [name="csrfmiddlewaretoken"]').attr('value');

    var form_data = {
        'province': $('#add-province').val(),
        'city': $('#add-city').val(),
        'exact_address': $('#add-exact_address').val(),
        'apartment_number': $('#add-No').val(),
        'unit': $('#add-unit').val(),
        'zip_code': $('#add-zip_code').val(),
    };

    $.ajax({
        type: "post",
        url: url,
        data: form_data,
        headers: {"X-CSRFToken": $crf_token},
        success: function (resp) {
            $('#add-address-form p').remove();
            form.trigger('reset');
            alert('« آدرس با موفقیت اضافه شد. »');
            $('#add-address-modal').modal('hide');
            window.location.href = "/orders/create-order/"

        },
        error: function (data) {
            $('#add-address-form p').remove();
            let errors = JSON.parse(data.responseText);
            for (let error_item in errors) {
                $(form).prepend(`<p class="text-danger">* ${errors[error_item][0]}</p>`);
            }
        }
    });

});