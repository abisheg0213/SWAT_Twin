import logo from './logo.svg';
import './App.css';
import React, { useEffect } from 'react';
import plant_design from "./plant_design.jpg"
import axios from 'axios';
import {io, Socket} from "socket.io-client"
import Popup from './components/Popup/Popup';

function App() {
  const [message,set_message]=React.useState({'Timestamp': '-', 'FIT101': 0, 'MV101':0, 'LIT101':302.455151121, 'P101': 0,'FIT201': 0, 'LIT201': 0, 'AIT201': 0, 'P201': 0,'P201_CL':1.5,'P202_CL':7.25,'P203_CL':4.5, 'AIT202': 0, 'P202': 0, 'AIT203': 0, 'P203': 0, 'P301': 0, 'FIT301': 0, 'LIT301': 0, 'AIT301': 0, 'DPH101': 0, 'PHP101': 0, 'FIT401': 0, 'MV401': 0, 'LIT401': 0, 'AIT401':0, 'AIT402':0, 'DP401': 0, 'DP402': 0, 'P401': 0, 'FIT501': 0, 'LIT101 Markers': {'CAP': 1500, 'LR': 200, 'HR': 1250}, 'LIT201 Markers': {'CAP': 1200, 'LR': 200, 'HR': 1250}, 'LIT301 Markers': {'CAP': 1200, 'LR': 200, 'HR': 1250}, 'LIT401 Markers': {'CAP': 1200, 'LR': 200, 'HR': 1250}, 'Chemical Markers': {'NaCl': 1.5, 'HCl': 7.25, 'NaOCl': 4.25, 'Cl2': 0.5, 'ORP': 750, 'TDS': 500}})
  const [popup_trig,set_popup_trigger]=React.useState(false)
  const [stage,setstage]=React.useState(1)
  const [component,set_component]=React.useState("")
  const closePop=()=>{
    console.log("called")
    set_popup_trigger(false)
  }

  const Button = ({ label, value, colorClass }) => (
    <div onClick={(e)=>{
      e.preventDefault()
      set_component(label)
      set_popup_trigger(true)
      
    }} className={`button ${colorClass}`}>
      <div className="button-label">{label}</div>
      <div className="button-value">{value}</div>
      
    </div>
  );
 
  // setInterval(()=>{
  //   axios.get("http://127.0.0.1:8000/get_data").then((res)=>{
  //     console.log(res.data)
  //     set_message(res.data)
  //   })
  // },1000)
  const sock=io('http://localhost:5000',{
    
  })
  sock.on('connect',()=>{
   console.log(" connected to server")
  })
  console.log(sock)
  sock.on('update_data',(data)=>{
    // console.log(data)
    set_message(data)
  })
  let components={1:['FIT101','MV101','LIT101','P101'],2:['FIT201','LIT201','AIT201','P201','AIT202','P202','AIT203','P203','P301'],3:['FIT301','LIT301','AIT301','DPH101','PHP101'],4:['FIT401','MV401','LIT401','AIT401','AIT402','DP401','DP402','P401','FIT501']}
  let actu_to_chemicals={'P201':'NaCl','P202':'HCl','P203':'NaOCl'}
  return (
   <div>
    <center>
    <img src={plant_design}></img>
    <br/>
    <div className="button-layout">
    <div className='status-bar'>
     {message['Timestamp']=="-" ? <>Plant Not Running</> : <>Plant Operating in Active Mode<br/> Timestamp : {message['Timestamp']}</>}
    </div>
    <div className="button-row">
          <div className="button" onClick={(e)=>{
            console.log("Stage-01")
            setstage(1)
          }}>Stage-01 Raw Water</div>
          <div className="button" onClick={(e)=>{
            console.log("Stage-02")
            setstage(2)
          }}>Stage-02 Chemical Filtration</div>
          <div className="button" onClick={(e)=>{
            console.log("Stage-03")
            setstage(3)
          }}>Stage-03 Dechlorination</div>
          <div className="button" onClick={(e)=>{
            console.log("Stage-04")
            setstage(4)
          }}>Stage-04 Reverse Osmosis</div>
        </div>
        <br/>
            <div className="buttons">
        <div className="button-row">
         {components[stage].map((data)=>{
          console.log(data)
          console.log(data.slice(0,3))
        if((data.slice(0,3)=="LIT" && (message[data].toFixed(3)>1200 || message[data].toFixed(3)<200))){
          return <Button label={data} value={message[data].toFixed(3)+" L"} colorClass="black"/>}
        else if((data.slice(0,3)=="LIT" && (message[data].toFixed(3)<1200 && message[data].toFixed(3)>200)))
        {
          return <Button label={data} value={message[data].toFixed(3)+" L"} colorClass="green"/>
        }
        else if(((data.slice(0,2)=="MV" || data.slice(0,4)=="P101" || data.slice(0,4)=="P301" || data.slice(0,4)=="P401")  && (message[data]==0)))
          {
            return <Button label={data} value="Closed" colorClass="red"/>
          }
          else if(((data.slice(0,2)=="MV" || data.slice(0,4)=="P101" || data.slice(0,4)=="P301" || data.slice(0,4)=="P401") && (message[data]!==0)))
            {
              return <Button label={data} value="Open" colorClass="green"/>
            }
            
            else if((data.slice(0,3)=="FIT" && (message[data]>3.5)))
              {
                console.log("FIT CASE1")
                return <Button label={data} value={message[data]+" cm3/s"} colorClass="blank"/>
              }
              else if((data.slice(0,3)=="FIT" && (message[data]==0)))
                {
                  console.log("FIT CASE2")
                  return <Button label={data} value={message[data]+" cm3/s"} colorClass="red"/>
                }
                else if((data.slice(0,3)=="FIT" && (message[data]>0 && message[data]<3.5)))
                  {
                    console.log("FIT CASE3")
                    console.log(data+"  "+message[data])
                    return <Button label={data} value={message[data]+"cm3/s"} colorClass="green"/>
                  }
                  else if(data.slice(0,3)=="AIT"){
                    return <Button label={data} value={message[data].toFixed(3)} colorClass=""/>
                  }
                  else if(data=="DPH101"){
                    return <Button label={data} value={"Ph Value = "+message[data]} colorClass=""/>
                  }
                  else if((data=="P201" || data=="P202" || data=="P203") && message[data]==0){
                    let str=data+"_CL"
                    return <Button label={data} value={"No Dosing added"+"\n"+"Chemical_limit :"+message[str]} colorClass="red"/>
                  }
                  else if((data=="P201" || data=="P202" || data=="P203") && message[data]!==0){
                    let str=data+"_CL"
                    return <Button label={data} value={"Dosing added "+message[data].toFixed(3)+"\n"+"Chemical_limit :"+message[str]} colorClass="green"/>
                  }
                  else if((data=="PHP101") && message[data]==0){
                    console.log("no neu")
                    return <Button label={data} value={"No base neutralisation done"} colorClass="red"/>
                  }
                  else if((data=="PHP101") && message[data]!==0){
                    console.log("yes neu")
                    return <Button label={data} value={message[data].toFixed(3)+" grams of NaHSO3 added"} colorClass="green"/>
                  }
                  else if((data=="DP401") && message[data]==0){
                    return <Button label={data} value={"No ORP nuetralisation"} colorClass="red"/>
                  }
                  else if((data=="DP401") && message[data]!==0){
                    return <Button label={data} value={message[data].toFixed(3)+" ORP nuetralisation"} colorClass="green"/>
                  }
                  else if((data=="DP402") && message[data]==0){
                    return <Button label={data} value={"No TPS nuetralisation"} colorClass="red"/>
                  }
                  else if((data=="DP402") && message[data]!==0){
                    return <Button label={data} value={message[data].toFixed(3)+" TPS nuetralisation"} colorClass="green"/>
                  }
                  else{
                    console.log("no choice found")
                  }
        })}
      
        </div>
      </div>
    
    </div>
    </center>
    <Popup trigger={popup_trig} value={message[component]} close={closePop}  component={component}/>
   </div>
  );
}

export default App;
