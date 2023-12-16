import { HashLink } from 'react-router-hash-link';
import cvat from '../static/cvat_report.png';
import v1 from '../static/v1.png';
import v2 from '../static/v2.png';
import v3 from '../static/v3.png';

function Report() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-center pb-14">Report</h1>

      <div className="flex flex-row">
        <div className="flex-none w-64 drawer lg:drawer-open">
          <input id="my-drawer-2" type="checkbox" className="drawer-toggle" />
          <div className="drawer-content flex flex-col items-center justify-center">
            {/* Page content here */}
            <label htmlFor="my-drawer-2" className="btn  drawer-button lg:hidden">
              Table of Contents
            </label>
          </div>
          <div className="drawer-side">
            <label
              htmlFor="my-drawer-2"
              aria-label="close sidebar"
              className="drawer-overlay"
            ></label>
            <ul className="rounded-md menu p-4 w-40 min-h-[50%] bg-base-200 text-base-content">
              <li>
                <HashLink to="#abstract">
                  <p>Abstract</p>
                </HashLink>
              </li>
              <li>
                <HashLink to="#introduction">
                  <p>Introduction</p>
                </HashLink>
              </li>
              <li>
                <HashLink to="#related-work">
                  <p>Related Work</p>
                </HashLink>
              </li>
              <li>
                <HashLink to="#technical-approach">
                  <p>Technical Approach</p>
                </HashLink>
              </li>
              <li>
                <HashLink to="#evaluation-and-results">
                  <p>Evaluation and Results</p>
                </HashLink>
              </li>
              <li>
                <HashLink to="#discussion-and-conclusions">
                  <p>Discussion and Conclusions</p>
                </HashLink>
              </li>
              <li>
                <HashLink to="#references">
                  <p>References</p>
                </HashLink>
              </li>
            </ul>
          </div>
        </div>

        <div className="flex flex-col">
          <div className="p-2" id="abstract">
            <div className="p-2 pb-1">
              <h2 className="text-2xl font-bold pb-5">Abstract</h2>
              <p>
                The objective is to figure out where a car is in a particular frame, extract
                keypoints, normalize the image, and feed the inputs to an LSTM model to predict what
                action the car took. The concerned outputs are <b>good</b>,<b>weaving</b>,{' '}
                <b>ran red light</b>, <b>crossing yellow line</b>, <b>off road</b>, and{' '}
                <b>collision</b>.
              </p>
            </div>
          </div>

          <div className="p-2" id="introduction">
            <div className="p-2 pb-1">
              <h2 className="text-2xl font-bold pb-5">Introduction</h2>
              <p>
                The goal is to use machine learning techniques to identify bad driving behaviors
                such as weaving in and out of a lane. There will be two models that will be trained.
                The first model built upon YOLOv8 will identify the car and plot visible keypoints
                as done in human pose landmarks. The second model will take that input, the image,
                and the red light sensor to determine the action as done in human action
                recognition.
              </p>
              <br />
              <p>
                Currently, trying to understand driving behavior is done using in-vehicle IMU data
                or in-vehicle cameras that observe the faces of drivers. One article [3] mentions
                the use of kinematics data to try to predict behaviors like fast U-turn, sudden
                braking, etc. Unfortunately, this becomes much more difficult when only using a
                monocular setup outside of the vehicle.
              </p>
              <br />
              <p>
                As stated, this approach tries to mimic the work done in human activity recognition
                and applies the same principles to view the car's motion through time. I believe it
                will be successful due to the potential impact of improving safety and response time
                to crashes or potential drunk driving. The biggest challenge is the complexity of
                the task and necessity of tons of training data. I needed to scale back due to how
                long it takes to train and annotate hundreds of images. Another challenge was the
                great dependency on the accuracy of the first model in identifying keypoints.
              </p>
              <br />
              <p>
                In order to execute, there needs to be lots of time dedicated to collecting and
                annotating data. As well, you need to make sure to have the computing resources
                since training takes a lot of time even with a powerful machine.
              </p>
              <p>
                The full pipeline will be tested by giving 10 never before seen videos of each
                action and evaluating how each version of the model predicts versus the ground
                truth.
              </p>
            </div>
          </div>

          <div className="p-2" id="related-work">
            <div className="p-2 pb-1">
              <h2 className="text-2xl font-bold pb-5">Related Work</h2>
              <h3 className="text-l font-bold py-2">Papers</h3>
              <p>
                The DMV criteria [1] is an inspiration for scoring a driver based on their behavior
                over time. Microsoft's research with HAMS [2] took it with one step further and
                described out using in-vehicle camera, they can sort of replace the driving
                instructor and the driving test more automated. The problem so far is that most
                articles deal with inside the vehicle and use sensors like the smartphone's
                accelerometer or the car's sensors. The third article which helped [3] dealt with
                training a LSTM-R to detect abnormal driving behavior. Again, the problem is using
                vehicle kinematic data using a smartphone. Using an LSTM is what I will be
                attempting and it was helpful to see behaviors like fast U-turns be something of
                interest as well.
              </p>
              <h3 className="text-l font-bold py-2">Datasets</h3>
              <p>Collected videos/images using CARLA simulator.</p>
              <h3 className="text-l font-bold py-2">Software</h3>
              <ul className="list-disc pl-5">
                <li>CARLA (source with Unreal Engine fork)</li>
                <li>Python 3.7.9 (CARLA)</li>
                <li>Python 3.9.0 (machine learning)</li>
                <li>YOLOv8 pose estimation</li>
                <li>CVAT annotation</li>
              </ul>
            </div>
          </div>

          <div className="p-2" id="technical-approach">
            <div className="p-2 pb-1">
              <h2 className="text-2xl font-bold pb-5">Technical Approach</h2>
              <p>
                The first step is to train on top of YOLOv8 pose estimation model [5] by collecting
                820 images each depicting several different car models and postions across the
                image. Using CVAT annotation software [6], the bounding box and 16 keypoints are
                manually drawn:
              </p>
              <br />
              <img src={cvat} width={800} height={800} />
              <br />
              <p>
                The car detection model is then trained which now can be used for phase two. The
                LSTM model will be responsible for detecting each of the several actions mentioned
                above. 40 videos at 10 frames each (5 seconds) is collected for each action. It is
                then fed into one of three LSTM models to train.
              </p>
              <br />
              <p>
                Version 1 uses the manual annotations on a subset of 15 videos for each of the
                actions besides off road and collision. The goal here is to see if given a highly
                accurate representation of the car movements, can it make accurate predictions.
                Version 2 and 3 free up the manual annotations constraint and rely heavily on the
                car detection model to extract the keypoints of the car. Version 2 uses the manual
                annotations from the subset and for the rest of the videos (and new actions), uses
                the detection model to extract. This is a sort of hybrid approach. Version 3 relies
                only on the car detection and instead extracts just the bounding box. There is a
                hypothesis that we may not even need any of the keypoints and just the bounding box
                will suffice. Notice that all three models are all still fed the red light sensor (0
                for green, 1 for red) and the pixels surrounding the car. The pixels surrounding the
                car should hopefully give context for determing where the car is relative to the
                yellow line, other cars, the intersection lines, etc.
              </p>
            </div>
          </div>

          <div className="p-2" id="evaluation-and-results">
            <div className="p-2 pb-1">
              <h2 className="text-2xl font-bold pb-5">Evaluation and Results</h2>
              <p>
                All models were trained using either a cropped image surrounding the car or the
                pixels in each corner of the bounding box. To maintain consistency, all models used
                the corner pixels approach.
              </p>
              <br />
              <h3 className="text-l font-bold py-2">Model 1</h3>
              <p>
                This model was trained using 15 videos over 4 actions. It uses manual annotations.
                It's accuracy with the test set was 22/40 (55%).
              </p>
              <ul className="list-disc pl-5">
                <li>good (2/10), avg confidence: 59%</li>
                <li>weaving (6/10), avg confidence: 58%</li>
                <li>red_light (10/10), avg confidence: 85%</li>
                <li>cross_yellow (6/10), avg confidence: 53%</li>
              </ul>
              <br />
              <img src={v1} width={300} height={300} />
              <br />
              <h3 className="text-l font-bold py-2">Model 2</h3>
              <p>
                This model was trained using 45 videos over 6 actions. It uses hybrid of available
                manual annotations and the car detection model for the rest. It's accuracy with the
                test set was 43/60 (71%).
              </p>
              <ul className="list-disc pl-5">
                <li>good (7/10), avg confidence: 51%</li>
                <li>weaving (7/10), avg confidence: 56%</li>
                <li>red_light (9/10), avg confidence: 81%</li>
                <li>cross_yellow (5/10), avg confidence: 55%</li>
                <li>off_road (9/10), avg confidence: 80%</li>
                <li>collision (6/10), avg confidence: 61%</li>
              </ul>
              <br />
              <img src={v2} width={300} height={300} />
              <br />
              <h3 className="text-l font-bold py-2">Model 3</h3>
              <p>
                This model was trained using 45 videos over 6 actions. It uses only the bounding box
                center coordinates from car detection model. It's accuracy with the test set was
                27/60 (45%).
              </p>
              <ul className="list-disc pl-5">
                <li>good (2/10), avg confidence: 33%</li>
                <li>weaving (4/10), avg confidence: 32%</li>
                <li>red_light (6/10), avg confidence: 63%</li>
                <li>cross_yellow (3/10), avg confidence: 38%</li>
                <li>off_road (6/10), avg confidence: 58%</li>
                <li>collision (6/10), avg confidence: 38%</li>
              </ul>
              <br />
              <img src={v3} width={300} height={300} />
              <br />
            </div>
          </div>

          <div className="p-2" id="discussion-and-conclusions">
            <div className="p-2 pb-1">
              <h2 className="text-2xl font-bold pb-5">Discussion and Conclusions</h2>
              <p>
                In conclusion, this was a difficult task which required an immense ammount of
                training data and effort to annotate the images. I'm happy with the results of the
                car detection model because that was once piece of worry because the LSTM models
                relies heavily on the accuracy. I feel like the lack of training data made the LSTM
                model suffer the most. This makes it hard to come to a compelling conclusion whether
                the keypoints were necessary. However, as the results show, the keypoints
                consistenly made model 2 average around 15% higher than model 3 when I was tuning
                the features and neural network.
              </p>
              <br />
            </div>
          </div>

          <div className="p-2" id="references">
            <div className="p-2 pb-1">
              <h2 className="text-2xl font-bold pb-5">References</h2>
              <ul className="list-decimal pl-5">
                <li>
                  State of California Department of Motor Vehicles, “Driving Performance Evaluation
                  (DPE) scoring criteria - California DMV,” California DMV, May 19, 2020.
                  https://www.dmv.ca.gov/portal/handbook/driving-test-criteria/driving-performance-evaluation-dpe-scoring-criteria/
                </li>
                <li>
                  “HAMS: Harnessing AutoMobiles for Safety - Microsoft Research,” Microsoft
                  Research, Jul. 18, 2022. https://www.microsoft.com/en-us/research/project/hams/
                </li>
                <li>
                  Y. Ma, Z. Xie, S. Chen, F. Qiao, and Z. Li, “Real-time detection of abnormal
                  driving behavior based on long short-term memory network and regression
                  residuals,” Transportation Research Part C: Emerging Technologies, vol. 146, p.
                  103983, Jan. 2023, doi: 10.1016/j.trc.2022.103983.
                </li>
                <li>
                  “Intersection safety,” FHWA.
                  https://highways.dot.gov/research/research-programs/safety/intersection-safety#:~:text=More%20than%2050%20percent%20of,occur%20at%20or%20near%20intersections.
                </li>
                <li>
                  Ultralytics. (n.d.-a). Pose. Ultralytics YOLOv8 Docs.
                  https://docs.ultralytics.com/tasks/pose/
                </li>
                <li>CVAT. (n.d.). https://www.cvat.ai/</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Report;
