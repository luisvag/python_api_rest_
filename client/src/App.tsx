import { Routes, Route } from 'react-router-dom'
import SignIn from './SignIn'
import SignUp from './SignUp'

export default function App() {
    return (
        <div className="App">
            <Routes>
                <Route path="/" element={<SignIn />} />
                <Route path="sign-up" element={<SignUp />} />
                {/* <Route path="reset-password" element={ <SignIn /> } /> */}
            </Routes>
        </div>
    )
}
