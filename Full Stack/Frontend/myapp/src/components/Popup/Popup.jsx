import React from "react"
import "./popup.css"
import { io } from "socket.io-client"
import { Button } from "react-bootstrap"
export default function Popup(props){
    let socket=io('http://localhost:5000')
    const [flow_input,set_flow_input]=React.useState(0)
    const [level_input,set_level_input]=React.useState(0)
    const [chemical_val,set_chemical_val]=React.useState(0)
    const [deviation_val,set_devi_val]=React.useState(0)
    console.log(props)
    // return (props.trigger) ? (<div className="popup">
    //     <div className="popup-inner">
    //         <h1>Component {props.component}</h1>
    //         <button onClick={(e)=>{
    //             e.preventDefault()
    //             props.close()
    //         }}>Close</button>
    //         </div>
    // </div>) : "";
    if(props.trigger)
        {
            if(props.component=="MV101" || props.component=="P101" || props.component=="P301" || props.component=="MV401" || props.component=="P401"){
                return <div className="popup"><div className="popup-inner">
                <h1>Component {props.component}</h1>
                <p>Stage - {props.value==1 ? "Open" :"Closed"}</p>
                <Button  variant="secondary" onClick={(e)=>{
                    e.preventDefault()
                   console.log("valve closed")
                   socket.emit('attack',{
                    'type':"valve",
                    'component':props.component,
                    'attack_type':"close"
                   })
          }}>Close Vavle</Button>
                <br/>
                <br/>
                <Button variant="secondary" onClick={(e)=>{
                    e.preventDefault()
                   console.log("valve opened")
                   socket.emit('attack',{
                    'type':"valve",
                    'component':props.component,
                    'attack_type':"open"
                   })
                }}>Open Vavle</Button> <br/><br/>
                <Button variant="secondary" onClick={(e)=>{
                    e.preventDefault()
                    props.close()
                }}>Close</Button>
                </div></div>
            }
            else if(props.component.slice(0,3)=='FIT')
            {
                return <div className="popup"><div className="popup-inner">
                <h1>Component {props.component}</h1>
                <p>Flow Rate - {props.value} cm3/s</p>
                
                {props.value !== 0 ? <div>
                <label>Enter new Flow rate</label>{"  "}
                <input onChange={(e)=>{
                    set_flow_input(e.target.value)
                }}></input><br/><br/>
                <Button  variant="secondary" onClick={(e)=>{
                    e.preventDefault()
                   console.log("flow rate changed")
                   console.log(flow_input)
                   socket.emit('attack',{
                    'type':"flowrate",
                    'component':props.component,
                    'flow_rate':Number(flow_input)
                   })
          }}>Change Flow Rate</Button>
          <br/><br/></div> : <></>}
          <Button variant="secondary" onClick={(e)=>{
                    e.preventDefault()
                    props.close()
                }}>Close</Button>
                
                
                </div></div>
            }
            else if(props.component.slice(0,3)=='LIT')
                {
                    return <div className="popup"><div className="popup-inner">
                    <h1>Component {props.component}</h1>
                    <p>Level Value - {props.value.toFixed(3)} L</p>
                    
                    {props.value !== 0 ? <div>
                        <p>Static Attack</p>
                    <label>Enter new Static Level Value</label>{"  "}
                    <input onChange={(e)=>{
                        set_level_input(e.target.value)
                    }}></input><br/><br/>
                    <Button  variant="secondary" onClick={(e)=>{
                        e.preventDefault()
                       console.log("flow rate changed")
                       console.log(flow_input)
                       socket.emit('attack',{
                        'type':"level_static_attack",
                        'component':props.component,
                        'level_val':Number(level_input)
                       })
              }}>Static Attack</Button>
              <br/><br/>
              <p>Gradual Attack</p>
                    <label>Enter Gradual deviation value</label>{"  "}
                    <input onChange={(e)=>{
                        set_devi_val(e.target.value)
                    }}></input><br/><br/>
                    <Button  variant="secondary" onClick={(e)=>{
                        e.preventDefault()
                       socket.emit('attack',{
                        'type':"level_gradual_attack",
                        'component':props.component,
                        'devi_val':Number(deviation_val)
                       })
              }}>Gradual Attack</Button>
              <br/><br/>
              </div> : <></>}
              <Button variant="secondary" onClick={(e)=>{
                        e.preventDefault()
                        props.close()
                    }}>Close</Button>
                    
                    
                    </div></div>
                }
                else if(props.component=='P201' || props.component=='P202' || props.component=='P203' )
                    {
                        return <div className="popup"><div className="popup-inner">
                        <h1>Component {props.component}</h1>
                        
                        <div>
                            <p>Chemical Maintance Attack</p>
                        <label>Enter new Chemical Limit Value</label>{"  "}
                        <input onChange={(e)=>{
                            set_chemical_val(e.target.value)
                        }}></input><br/><br/>
                        <Button  variant="secondary" onClick={(e)=>{
                            e.preventDefault()
                           console.log("flow rate changed")
                           console.log(flow_input)
                           socket.emit('attack',{
                            'type':"chemical_attack",
                            'component':props.component,
                            'chemical_val':Number(chemical_val)
                           })
                  }}>Chemical Attack</Button>
                  <br/><br/>
                  
                  </div> 
                  <Button variant="secondary" onClick={(e)=>{
                            e.preventDefault()
                            props.close()
                        }}>Close</Button>
                        
                        
                        </div></div>
                    }
        }
}
