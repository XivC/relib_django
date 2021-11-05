class Book extends React.Component {



    render() {
        return <div className="book col">

            <div className="title">{this.props.title}</div>
            <div className="author">{this.props.author}</div>

        </div>
    }



}