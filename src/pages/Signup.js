import { useNavigate } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";
import "../pages/Signup.css";


const Signup = () => {
  const navigate = useNavigate();

  return (
    <div className="signup-container">
      <h2>Sign Up</h2>
      <Formik
        initialValues={{ username: "", email: "", password: "" }}
        validationSchema={Yup.object({
          username: Yup.string().required("Username is required"),
          email: Yup.string().email("Invalid email").required("Email is required"),
          password: Yup.string().min(6, "Password must be at least 6 characters").required("Password is required"),
        })}
        onSubmit={async (values, { setSubmitting, setErrors }) => {
          try {
            const res = await fetch("http://127.0.0.1:5000/users", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(values),
            });
            const data = await res.json();
            if (res.ok) {
              navigate("/login");
            } else {
              setErrors({ general: data.error || "Signup failed" });
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

            <label>Email</label>
            <Field name="email" type="email" />
            <ErrorMessage name="email" component="div" className="error" />

            <label>Password</label>
            <Field name="password" type="password" />
            <ErrorMessage name="password" component="div" className="error" />

            {errors.general && <div className="error">{errors.general}</div>}

            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Signing up..." : "Sign Up"}
            </button>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default Signup;
