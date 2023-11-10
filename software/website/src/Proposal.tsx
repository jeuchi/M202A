function Proposal() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-center pb-14">Proposal</h1>
      <div>
        <div className="p-2">
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-5">Motivation & Objective</h2>
            <p>
              The objective is to use machine learning in order to classify hard to detect behaviors
              on the road. For example, someone may be under the influence and could potentially
              cause a collision.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-5">State of the Art & Its Limitations</h2>
            <p>
              There hasn't been an exact attempt at this problem. AI has been used for DMV test
              (HAMS under Microsoft). AI has also been trained to detect similar car behaviors that
              this project is attempting to detect such as weaving, fast U-turn, etc. However, most
              of the time, these experiments use in-vehicle kinematics where this project simply has
              a camera at an intersection.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-5">Novelty & Rationale</h2>
            <p>
              Compared to other experiments, this attempts to redefine traffic light capabilities.
              We don't have information inside the vehicle and must make our determinations from
              video footage. I think it will be successful because it is analogous to trying to
              determine human action such as reading sign language or human emotion or human
              actions.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-5">Potential Impact</h2>
            <p>
              If successful, it can be a helpful tool for law enforcement and prevention of
              accidents. Most accidents occur at intersections (???) and it will be useful if AI
              could assist in prevention. As well, the most severe detection is a collision and
              alerting emergency services early can make the difference in life and death.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-5">Challenges</h2>
            <p>There are several critical areas when coming up with the pipeline.</p>
            <h3 className="text-l font-bold py-2">1. Data</h3>
            <p>
              Training different neural networks requires an immense amount of training computation
              and effort to make sure there are sufficient and useful data. As well, there is a
              complexity in selecting features to extract from.
            </p>
            <h3 className="text-l font-bold py-2">2. Reality</h3>
            <p>
              The real-world enviornment may not be as nice as in the simulator. We are also
              assuming perfect clarity and reliable data collection.
            </p>
            <h3 className="text-l font-bold py-2">3. Human Behavior</h3>
            <p>
              Trying to model complex human behaviors when driving requires several different
              metrics. For example, even in weaving, we cannot make the call to flag down an officer
              with one event. It requires different degrees of weaving (near miss) and several
              observations over time. The temporal nature of this problem requires keeping a score
              of the driver.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-5">Requirements of Success</h2>
            <p>
              The requirements for success are confident predictions of actions to specific cars in
              the scene. It's useless if make poor predicitions.
            </p>
            <h2 className="text-2xl font-bold pb-5">Metrics of Success</h2>
            <p>
              Since we are using confidence, we need to make sure our model's confidence is not only
              high, but accuracy is high. A highly confident but incorrect model points to a flaw in
              the training.
            </p>
            <h2 className="text-2xl font-bold pb-5">Execution Plan</h2>
            <p></p>
            <h2 className="text-2xl font-bold pb-5">Related Work</h2>
            <p></p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Proposal;
