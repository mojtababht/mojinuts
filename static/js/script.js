$(document).ready(
    // signup login logout
    () => {
        $('.login-signup input').attr('class', 'form-control form-control-lg')

        $('#id_first_name').prop('required', true)

        $('#logoutLink').click(
            () => {
                if (confirm("از درخواست خود اطمینان دارید؟")) {
                    window.open('/accounts/logout', '_self')
                    localStorage.setItem('previousUrl', window.location.href)


                }

            }
        )
        $('#loginsubmit').submit(
            () => {
                localStorage.setItem('previousUrl', document.referrer)
            }
        )
        //signup login logout

        $('.city-list').hover(
            function () {

                $(this).addClass('active')
            }
            ,
            function () {
                $(this).removeClass('active')
            }
        )

        $('select#id_city').addClass('form-select').css('width','fit-content').select2()
        $('#ordercity').select2()

        $('select#id_inventory').addClass('form-select').addClass('form-control').css('width','fit-content').select2()
        $('select#id_product').addClass('form-select').addClass('form-control').css('width','fit-content').select2()
        $('#id_quantity').addClass('form-control')
        $('#newproduct input').addClass('form-control')
        $('#newproduct select').addClass('form-select')







    })