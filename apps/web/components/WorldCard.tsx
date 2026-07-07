type Props={world:{day:number;population:number;energy:number;water:number;food:number}}

export default function WorldCard({world}:Props){
return (<section style={{border:'1px solid #ddd',padding:16,borderRadius:8,maxWidth:420}}>
<h2>Ares Alpha</h2>
<p>Day {world.day}</p>
<p>Population: {world.population}</p>
<p>Energy: {world.energy}%</p>
<p>Water: {world.water}%</p>
<p>Food: {world.food}%</p>
</section>)
}
