
    function showSignup() {
        document.getElementById('login').style.display = 'none';
        document.getElementById('signup').style.display = 'flex';
    }

    function showLogin() {
        document.getElementById('signup').style.display = 'none';
        document.getElementById('login').style.display = 'flex';
    }

    function otp() {
        document.getElementById('signup').style.display = 'none';
        document.getElementById('OTP').style.display = 'flex';
    }


    document.getElementById('signupForm').addEventListener('submit', getdata);
    var originalotp;
    var params;

    function getdata(e) {
        e.preventDefault();

        var name = document.getElementsByName('name')[0].value;
        var email = document.getElementsByName('email')[0].value;
        var password = document.getElementsByName('password')[0].value;
        var repassword = document.getElementsByName('repassword')[0].value;
        if (password == repassword) {

            params = {
                    name: name,
                    email: email,
                    password: password,
                    repassword: repassword
                }
                // const wrapper = document.getElementById('wrapper');
                // // Hide the wrapper initially
                // wrapper.style.display = 'block';
                // send http request to our backend program of add funciton to add data in our database
            var xhr = new XMLHttpRequest()
            xhr.open('post', '../signupForm', true)
            xhr.setRequestHeader('Content-type', 'application/json')
            xhr.onreadystatechange = function() {
                    //when the data will be loaded then the form section will be closed
                    if (xhr.readyState == 4) {
                        if (xhr.status == 200) {
                            console.log(this.responseText)
                            var data = JSON.parse(this.responseText)
                            if (data['email']) {
                                originalotp = data['otp']

                            } else {
                                document.getElementById('hidden').innerText = 'email not found'
                            }

                        } else {
                            // Handle the error response
                            console.log('error')
                        }
                    }

                    //this function is use to create dynamic html content by using two parameter name and data
                    // this is use to reset the form and not to store privous data
                    // var element = document.getElementById('postform');
                    // element.reset();
                    //document.getElementById('prediction').innerHTML= this.responseText;
                }
                //send data in json format
            xhr.send(JSON.stringify(params));
        } else {
            document.getElementById('hidden').innerText = 'password not matched'
        }

    }
    document.getElementById('otpForm').addEventListener('submit', submitOTP);

    function submitOTP(e) {
        e.preventDefault();

        // Get OTP input values
        var input1 = document.getElementById('input1').value;
        var input2 = document.getElementById('input2').value;
        var input3 = document.getElementById('input3').value;
        var input4 = document.getElementById('input4').value;

        var otp = input1 + input2 + input3 + input4;
        if (otp == originalotp) {
            var xhr = new XMLHttpRequest()
            xhr.open('post', '../signupFormCompleted', true)
            xhr.setRequestHeader('Content-type', 'application/json')
            xhr.onreadystatechange = function() {
                //when the data will be loaded then the form section will be closed
                if (xhr.readyState == 4) {
                    if (xhr.status == 200) {
                        if (params) {
                            data = JSON.parse(this.responseText)
                            client_id = data['client_id']
                            window.location.href = `/user_page/${client_id}`;
                        }

                    } else {
                        // Handle the error response
                        console.log('error')
                    }
                }
            }
            xhr.send(JSON.stringify(params));
        } else {


            document.getElementsByClassName('message').innerText = 'wrong otp enter again'
        }

    }
    document.getElementById('login').addEventListener('submit', login);

    function login(e) {
        e.preventDefault();

        var email = document.getElementsByName('loginemail')[0].value;
        var password = document.getElementsByName('loginpassword')[0].value;
        console.log(email, password)
        var paramss = {
            email: email,
            password: password
        };

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/login', true);
        xhr.setRequestHeader('Content-type', 'application/json');

        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    // Handle the successful response
                    var data = JSON.parse(this.responseText);
                    if (data['client_id']) {
                        // Successful login logic here
                        client_id = data['client_id']
                        window.location.href = `/user_page/${client_id}`;
                        console.log('Login successful');
                    } else {
                        document.getElementById('hidden2').innerText = 'incorrect details';
                    }
                } else {
                    // Handle the error response
                    console.log('Error during login');
                }
            }
        };

        xhr.send(JSON.stringify(paramss));
    }
