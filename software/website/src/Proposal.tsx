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
              cause a collision. Or if there is a collision, having the fastest possible response
              time to save lives at the scene. The other usage is to aid in finding drivers who
              exhibit dangerous driving behaviors.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-5">State of the Art & Its Limitations</h2>
            <p>
              There hasn't been an exact attempt at this problem. AI has been used for DMV test
              (HAMS under Microsoft) [2]. AI has also been trained to detect similar car behaviors
              that this project is attempting to detect such as weaving, fast U-turn, etc. However,
              most of the time, these experiments use in-vehicle kinematics where this project
              simply has a camera at an intersection.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-5">Novelty & Rationale</h2>
            <p>
              Compared to other experiments, this attempts to redefine traffic light capabilities.
              We don't have information inside the vehicle and must make our determinations from
              video footage. I think it will be successful because it is analogous to trying to
              determine human action such as reading sign language, human emotions or human actions.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-5">Potential Impact</h2>
            <p>
              If successful, it can be a helpful tool for law enforcement and prevention of
              accidents. More than 50% of fatal and injury accidents occur at intersections [4] and
              it will be useful if AI could assist in prevention. As well, the most severe detection
              is a collision and alerting emergency services early can make the difference in life
              and death.
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
              the scene. It's useless if we make poor predicitions.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-5">Metrics of Success</h2>
            <p>
              Since we are using confidence, we need to make sure our model's confidence is not only
              high, but accuracy is high. A highly confident but incorrect model points to a flaw in
              the training.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-5">Execution Plan</h2>
            <p>
              The plan is to train a model using YOLOv8 to extract car key points. We will get the
              bounding box, tire positions, front license plate, back license plate, etc. Taking
              those keypoints, red light sensor, speed limit, and the image, we will train a RNN to
              determine the car's actions from a sequence of frames. The model will output either
              weaving, near miss, ran red light, good driving, etc. In the CARLA simulator, will
              take the bounding box of the output and capture a zoomed-in photo. This will be fed
              into a model to read the license plate. Collecting all the information together, we
              can update a database which will contain a rating for this driver. They will start at
              5 stars and each action has a certain weight which will decrease the score. An
              immediate action like a collision or red light violation will trigger the authorities.
              Otherwise, repeated bad actions will trigger the authorities once the rating drops
              below a certain threshold.
            </p>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-5">Related Work</h2>
            <h3 className="text-l font-bold py-2">Papers</h3>
            <p>
              The DMV criteria [1] is an inspiration for scoring a driver based on their behavior
              over time. Microsoft's research with HAMS [2] took it with one step further and
              described out using in-vehicle camera, they can sort of replace the driving instructor
              and the driving test more automated. The problem so far is that most articles deal
              with inside the vehicle and use sensors like the smartphone's accelerometer or the
              car's sensors. The third article which helped [3] dealt with training a LSTM-R to
              detect abnormal driving behavior. Again, the problem is using vehicle kinematic data
              using a smartphone. Using an LSTM is what I will be attempting and it was helpful to
              see behaviors like fast U-turns be something of interest as well.
            </p>
            <h3 className="text-l font-bold py-2">Datasets</h3>
            <p>TBD</p>
            <h3 className="text-l font-bold py-2">Software</h3>
            <ul className="list-disc pl-5">
              <li>CARLA (source with Unreal Engine fork)</li>
              <li>Python 3.7.9</li>
              <li>YOLOv8</li>
            </ul>
          </div>
          <div className="p-2 pb-1">
            <h2 className="text-2xl font-bold pb-5">References</h2>
            <ul className="list-decimal pl-5">
              <li>
                State of California Department of Motor Vehicles, “Driving Performance Evaluation
                (DPE) scoring criteria - California DMV,” California DMV, May 19, 2020.
                https://www.dmv.ca.gov/portal/handbook/driving-test-criteria/driving-performance-evaluation-dpe-scoring-criteria/
              </li>
              <li>
                “HAMS: Harnessing AutoMobiles for Safety - Microsoft Research,” Microsoft Research,
                Jul. 18, 2022. https://www.microsoft.com/en-us/research/project/hams/
              </li>
              <li>
                Y. Ma, Z. Xie, S. Chen, F. Qiao, and Z. Li, “Real-time detection of abnormal driving
                behavior based on long short-term memory network and regression residuals,”
                Transportation Research Part C: Emerging Technologies, vol. 146, p. 103983, Jan.
                2023, doi: 10.1016/j.trc.2022.103983.
              </li>
              <li>
                “Intersection safety,” FHWA.
                https://highways.dot.gov/research/research-programs/safety/intersection-safety#:~:text=More%20than%2050%20percent%20of,occur%20at%20or%20near%20intersections.
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Proposal;
