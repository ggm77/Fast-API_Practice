import React, { useState }  from "react";
import { Button, Form } from 'react-bootstrap';

const Login = () => {

    return(
        <div>
            <h2>Login</h2>
            <Form method="POST" action="http://localhost:8000/loginProcess">
                <h4>Id</h4>
                <input type="text" name="username"></input>
                <br/><br/>
                <h4>Passowrd</h4>
                <input type="password" name="password"></input>
                <br/><br/>
                <Button variant="primary" type="submit">
                    Submit
                </Button>
            </Form>
        </div>
    );
};

export default Login;