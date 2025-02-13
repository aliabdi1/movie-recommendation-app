import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import "../pages/login.css";


const Login = () => {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  return (
    <div className="login-container">
      <h2>Login</h2>
      <Formik
        initialValues={{ username: "", password: "" }}
        validationSchema={Yup.object({
          username: Yup.string().required("Username is required"),
          password: Yup.string().required("Password is required"),
        })}
        onSubmit={async (values, { setSubmitting, setErrors }) => {
          try {
            const res = await fetch("http://127.0.0.1:5000/login", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(values),
            });
            const data = await res.json();
            if (res.ok) {
              login(data.access_token);
              navigate("/movies");
            } else {
              setErrors({ general: "Invalid username or password" });
            }
          } catch (error) {
            setErrors({ general: "Server error, try again later" });
          }
          setSubmitting(false);
        }}
      >
        {({ errors, isSubmitting }) => (
          <Form>
            <label>Username</label>
            <Field name="username" type="text" />
            <ErrorMessage name="username" component="div" className="error" />

            <label>Password</label>
            <Field name="password" type="password" />
            <ErrorMessage name="password" component="div" className="error" />

            {errors.general && <div className="error">{errors.general}</div>}

            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Logging in..." : "Login"}
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default Login;
