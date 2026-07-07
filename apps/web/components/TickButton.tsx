'use client'

export default function TickButton(){
 async function advance(){
  await fetch('/api/tick',{method:'POST'})
  window.location.reload()
 }
 return <button onClick={advance}>Advance One Day</button>
}
