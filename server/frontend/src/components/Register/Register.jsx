import React, { useState } from 'react';
import "./Register.css";
import Header from '../Header/Header';

const Register = () => {
    const [userName, setUserName] = useState("");
    const [password, setPassword] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState("");

    const register = async (e) => {
        e.preventDefault();
        let register_url = window.location.origin + "/djangoapp/register";

        const res = await fetch(register_url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "userName": userName,
                "password": password,
                "firstName": firstName,
                "lastName": lastName,
                "email": email
            }),
        });

        const json = await res.json();
        if (json.status != null && json.status === "Authenticated") {
            sessionStorage.setItem('username', json.userName);
            window.location.href = window.location.origin;
        }
        else if (json.error === "Already Registered") {
            alert("The user with same username is already registered.");
        }
    };

    return (
        <div>
            <Header />
            <div className="register_container">
                <form className="login_panel" onSubmit={register}>
                    <div>
                        <span className="input_field">Username </span>
                        <input type="text" name="username" placeholder="Username" className="input_field" onChange={(e) => setUserName(e.target.value)} required />
                    </div>
                    <div>
                        <span className="input_field">First Name </span>
                        <input type="text" name="first_name" placeholder="First Name" className="input_field" onChange={(e) => setFirstName(e.target.value)} required />
                    </div>
                    <div>
                        <span className="input_field">Last Name </span>
                        <input type="text" name="last_name" placeholder="Last Name" className="input_field" onChange={(e) => setLastName(e.target.value)} required />
                    </div>
                    <div>
                        <span className="input_field">Email </span>
                        <input type="email" name="email" placeholder="Email" className="input_field" onChange={(e) => setEmail(e.target.value)} required />
                    </div>
                    <div>
                        <span className="input_field">Password </span>
                        <input name="psw" type="password" placeholder="Password" className="input_field" onChange={(e) => setPassword(e.target.value)} required />
                    </div>
                    <div>
                        <input className="action_button" type="submit" value="Register" />
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Register;
