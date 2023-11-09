function Proposal() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-center pb-14">Proposal</h1>
      <div>
        <div className="p-2">
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-2">Motivation & Objective</h2>
            <p>
              The objective is to use machine learning in order to classify hard to detect behaviors
              on the road. For example, someone may be under the influence and could potentially
              cause a collision.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-2">State of the Art & Its Limitations</h2>
            <p>
              There hasn't been an exact attempt at this problem. AI has been used for DMV test
              (HAMS under Microsoft). AI has also been trained to detect similar car behaviors that
              this project is attempting to detect such as weaving, fast U-turn, etc. However, most
              of the time, these experiments use in-vehicle kinematics where this project simply has
              a camera at an intersection.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-2">Novelty & Rationale</h2>
            <p>
              Compared to other experiments, this attempts to redefine traffic light capabilities.
              We don't have information inside the vehicle and must make our determinations from
              video footage. I think it will be successful because it is analogous to trying to
              determine human action such as reading sign language or human emotion or human
              actions.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-2">Potential Impact</h2>
            <p>
              If successful, it can be a helpful tool for law enforcement and prevention of
              accidents. Most accidents occur at intersections (???) and it will be useful if AI
              could assist in prevention. As well, the most severe detection is a collision and
              alerting emergency services early can make the difference in life and death.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-2">Challenges</h2>
            <p></p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-2">Requirements of Success</h2>
            <p></p>
            <h2 className="text-2xl font-bold pb-2">Metrics of Success</h2>
            <p></p>
            <h2 className="text-2xl font-bold pb-2">Execution Plan</h2>
            <p></p>
            <h2 className="text-2xl font-bold pb-2">Related Work</h2>
            <p></p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Proposal;
