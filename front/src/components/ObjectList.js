import React from 'react'
import axios from 'axios'

class ObjectList extends React.Component {

state = {
  object_list : [],
  entered_objects : [],
  exited_objects : [],
}

componentDidMount = ()=>{
let url = 'http://127.0.0.1:8000/api/object/'
this.intervale = setInterval(()=>{
  axios.get(url).then((res)=>{
  //  this.setState({object_list:res.data})
    //console.log(res.data);
    let entered_objects = res.data.filter(obj=>obj.entered == true)
    let exited_objects = res.data.filter(obj=>obj.entered == false)
    this.setState({entered_objects:entered_objects})
    this.setState({exited_objects:exited_objects})
  }).catch((error)=>{
  console.log(error);
  })
},3000)

}
render(){
return(
<div class='container'>
<div class='row' style={{marginTop:'20px'}}>
<div class='col-lg-6'>
<center><h3>Entered({this.state.entered_objects.length})</h3></center>
<div class='row' style={{backgroundColor : '#ef9921',padding:'20px',marginRight : '5px',borderRadius:'25px'}}>
{this.state.entered_objects.map((obj)=>{
  return(
    <div key={obj.id} class='col-lg-12'>
    <img src={obj.image} class='img-fluid' width='100%' height='300px' style={{borderRadius:'25px'}} />
    <center><h5>{obj.name}</h5></center>
    <hr style={{backgroundColor:'white',height:'2px'}}/>
    </div>
  )
})}
</div>
</div>
<div class='col-lg-6'>
<center><h3>Exited({this.state.exited_objects.length})</h3></center>
<div class='row' style={{backgroundColor : '#4286f4',padding:'20px',marginLeft:'5px',borderRadius:'25px'}} >
{this.state.exited_objects.map((obj)=>{
  return(
    <div key={obj.id} class='col-lg-12'>
    <img src={obj.image} class='img-fluid' style={{borderRadius:'25px'}} />
    <center><h5>{obj.name}</h5></center>
    <hr style={{backgroundColor:'white',height:'2px'}}/>
    </div>
  )
})}
</div>
</div>
</div>
</div>
)


}



}
export default ObjectList ;
