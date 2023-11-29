import { HashLink } from 'react-router-hash-link';

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
                action the car took. For sake of time, the concerned outputs are <b>good</b>,{' '}
                <b>weaving</b>, and <b>ran red light</b>.
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
                or in-vehicle cameras that observe the faces of drivers. One article [TODO] mentions
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
              <p>Success...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Report;
