export default async function Home() {
  const res = await fetch('http://localhost:8000/world', { cache: 'no-store' }).catch(() => null)
  const world = res ? await res.json() : null

  return (
    <main style={{padding:40,fontFamily:'sans-serif'}}>
      <h1>🌍 CivilOS · Ares Alpha</h1>
      {world ? (
        <>
          <p>Day {world.day}</p>
          <p>Population: {world.population}</p>
          <p>Energy: {world.energy}%</p>
          <p>Water: {world.water}%</p>
          <p>Food: {world.food}%</p>
        </>
      ) : <p>Waiting for API...</p>}
    </main>
  )
}
