class Profile extends React.Component {



    render() {
        return (
            <div>
                <div>ID пользователя:</div> 
            <div className="input-group mb-3">
                
                <input type="number" className="form-control" id="id" defaultValue={this.props.userId}/>
       
                <div className="input-group-append">
                    
                    <button className="btn btn-outline-secondary" type="button" onClick={() => {
                        this.props.setUserId(document.getElementById("id").value);
                    }}>Отправить</button>
                </div>
            </div>
            </div>)

    }
}