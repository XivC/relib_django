class Tab extends React.Component {


  onClick = () => {
    const { label, onClick } = this.props;
    onClick(label);
  }

  render() {
    const {
      onClick,
      props: {
        activeTab,
        label,
      },
    } = this;

    let className = 'tab-list-item col';

    if (activeTab === label) {
      className += ' tab-list-active';
    }

    return (
      <div
        className={className}
        onClick={onClick}
      >
        {label}
      </div>
    );
  }
}
