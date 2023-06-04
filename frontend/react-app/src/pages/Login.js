import React, { useState } from 'react';


const Login = () => {

    const [username, setUsername] = useState();
    const [password, setPassword] = useState();

    const fData = new FormData();

    fData.append("username",username);
    fData.append("password", password);

    const handleSubmit = (e) => {
        e.preventDefault();
        fetch('http://localhost:8000/token', {
            method: 'POST',
            body: fData,
          }
            
        )
            .then(response => response.json())
            .then(res => console.log(res))
            
        };


    return(
        <div className='login-wrapper'>
            <form>
                <h1>Login</h1>
                <label>
                    <p>Username</p>
                    <input type='text' onChange={e => setUsername(e.target.value)}/>
                </label>
                <label>
                    <p>Password</p>
                    <input type='password' onChange={e => setPassword(e.target.value)}/>
                </label>
                <div>
                    <button onClick={ handleSubmit }>Submit</button>
                </div>
            </form>
        </div>
    );
};

export default Login;