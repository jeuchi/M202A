function Home() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-center">Introduction to TrafficWatch</h1>

      <div className="p-2">
        <h1 className="text-2xl font-bold pb-1">Abstract</h1>
        <p>
          The goal is to detect bad driving behaviors using machine learning using a single camera
          overlooking an intersection. Can we detect either <b>good driving</b>,<b>weaving</b>,
          <b>running the red light</b>, <b>crossing the yellow line</b>, <b>going off road</b>, or a{' '}
          <b>collision</b>. This approach avoids using in-vehicle IMU data and instead relies on
          computer vision to determine how the car is moving in the scene.
        </p>
      </div>
      <div className="p-2 pb-1">
        <h2 className="text-2xl font-bold">Team</h2>
        <p>Jeremy Euchi</p>
      </div>
    </div>
  );
}

export default Home;
