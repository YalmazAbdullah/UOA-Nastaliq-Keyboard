import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import KeyboardImeNaive from './components/KeyboardImeNaive'
import KeyboardCrulp from './components/KeyboardCrulp'
import KeyboardWindows from './components/KeyboardWindows'
import KeyboardTest from './components/KeyboardTest'
import KeyboardIme from './components/KeyboardIme'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
    <div>
      <KeyboardIme />
    </div>
    </>
  )
}

export default App
