
import { useState } from "react";
import "./App.css";
import "leaflet/dist/leaflet.css";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  useMap,
} from "react-leaflet";

function RepairMap({ center }) {
  
  if (!center) return null;

  return (
    <MapContainer
      center={[center.latitude, center.longitude]}
      zoom={13}
      style={{
  height: "350px",
  width: "100%",
  minHeight: "350px",
  borderRadius: "18px",

      }}
    >
      <TileLayer
        attribution='&copy; OpenStreetMap contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <Marker
        position={[center.latitude, center.longitude]}
      >
        <Popup>
          <strong>{center.name}</strong>
          <br />
          {center.address}
          <br />
          {center.distance_km} km away
        </Popup>
      </Marker>
    </MapContainer>
  );
}

function App() {
  const [category, setCategory] = useState("");
  const [description, setDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [center, setCenter] = useState(null);
  const [centerLoading, setCenterLoading] = useState(false);

 const handleSubmit = async (e) => {
  e.preventDefault();

  if (!category || !description) return;

  setLoading(true);
  setResult(null);

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/api/repair/process/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          category,
          description,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Something went wrong");
    }

    setResult(data);

  } catch (error) {
    console.error(error);
    setResult({
      verdict: "error",
      reason: "We couldn't check your device right now. Please try again.",
    });
  } finally {
    setLoading(false);
  }
};

const findEwasteCenter = async () => {
  setCenterLoading(true);
  setCenter(null);

  if (!navigator.geolocation) {
    setCenter({
      error: "Location is not supported by your browser.",
    });
    setCenterLoading(false);
    return;
  }

  navigator.geolocation.getCurrentPosition(
    async (position) => {
      const latitude = position.coords.latitude;
      const longitude = position.coords.longitude;

      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/collection/nearest/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              category,
              latitude,
              longitude,
            }),
          }
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.message || "No collection center found"
          );
        }

        setCenter(data);

      } catch (error) {
        console.error(error);

        setCenter({
          error: "We couldn't find a suitable e-waste center right now.",
        });
      } finally {
        setCenterLoading(false);
      }
    },

    () => {
      setCenter({
        error: "We couldn't access your location. Please allow location access and try again.",
      });

      setCenterLoading(false);
    }
  );
};

  return (
    <div className="app">

      {/* NAVBAR */}
      <nav className="navbar">
        <div className="logo">
          <div className="logo-icon">♻</div>
          <span>EcoRepair</span>
        </div>

        <div className="nav-links">
          <a href="#how">How it works</a>
          <a href="#impact">Our impact</a>
          <button className="nav-button">Get Started</button>
        </div>
      </nav>

      {/* HERO */}
      <main>
        <section className="hero">
          <div className="hero-content">

            <div className="eyebrow">
              <span>✦</span>
              AI-powered sustainable repair
            </div>

            <h1>
              Don't replace it.
              <br />
              <span>Repair it.</span>
            </h1>

            <p className="hero-text">
              Tell us what's wrong with your electronic device.
              EcoRepair helps you understand whether it's worth fixing
              — and guides you to responsible disposal when it isn't.
            </p>

            <div className="hero-actions">
              <button
                className="primary-button"
                onClick={() =>
                  document
                    .getElementById("checker")
                    .scrollIntoView({ behavior: "smooth" })
                }
              >
                Check my device
                <span>→</span>
              </button>

              <div className="trust">
                <div className="trust-icon">🌱</div>

                <div>
                  <strong>Repair before replacing</strong>
                  <small>Make smarter device decisions</small>
                </div>
              </div>
            </div>

          </div>

          {/* DEVICE CHARACTER */}
          <div className="mascot-area">
            <div className="glow"></div>

            <div className="floating-chip chip-one">
              ♻ Repair
            </div>

            <div className="floating-chip chip-two">
              ⚡ AI Advisor
            </div>

            <div className="floating-chip chip-three">
              🌱 Less waste
            </div>

            <div className="device-character">

              <div className="device-screen">
                <div className="face">
                  <span className="eye left"></span>
                  <span className="eye right"></span>
                  <span className="mouth">⌣</span>
                </div>

                <div className="screen-glow"></div>
              </div>

              <div className="device-base"></div>

              <div className="device-feet">
                <span></span>
                <span></span>
              </div>

              <div className="spark spark-one">✦</div>
              <div className="spark spark-two">✦</div>

            </div>
          </div>
        </section>

        {/* CHECKER */}
        <section className="checker-section" id="checker">

          <div className="section-heading">
            <div className="section-tag">
              01 / REPAIR ADVISOR
            </div>

            <h2>
              What's wrong
              <br />
              with your device?
            </h2>

            <p>
              Give us a few details. Our repair advisor will look
              for known fault patterns and give you a practical recommendation.
            </p>
          </div>

          <div className="checker-card">

            <form onSubmit={handleSubmit}>

              <div className="form-group">
                <label>What device is it?</label>

                <div className="select-wrapper">
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                  >
                    <option value="">
                      Select a device
                    </option>

                    <option value="mobile">
                      📱 Mobile
                    </option>

                    <option value="laptop">
                      💻 Laptop
                    </option>

                    <option value="fan">
                      🌀 Fan
                    </option>

                    <option value="mixer">
                      🥣 Mixer / Grinder
                    </option>

                    <option value="washing_machine">
                      🧺 Washing Machine
                    </option>

                    <option value="refrigerator">
                      🧊 Refrigerator
                    </option>

                    <option value="other">
                      🔌 Other
                    </option>
                  </select>
                </div>
              </div>

              <div className="form-group">

                <label>What's happening?</label>

                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Example: My laptop gets very hot and suddenly shuts down..."
                  rows="5"
                ></textarea>

                <div className="character-hint">
                  <span>💡</span>
                  Describe the problem in your own words.
                </div>

              </div>

              <button
                className="check-button"
                type="submit"
              >
                Check repairability
                <span>✦</span>
              </button>

            </form>

            {loading && (
  <div className="result-card loading-result">
    <div className="result-icon">🧠</div>
    <div>
      <h3>Checking your device...</h3>
      <p>Our repair advisor is looking for matching fault patterns.</p>
    </div>
  </div>
)}

{result && !loading && (
  <div className={`result-card ${result.verdict}`}>

    <div className="result-icon">
      {result.verdict === "repairable" && "🔧"}
      {result.verdict === "uncertain" && "🔍"}
      {result.verdict === "not_economical" && "♻️"}
      {result.verdict === "error" && "⚠️"}
    </div>

    <div className="result-content">

      <div className="result-label">
        YOUR REPAIR ADVISOR RESULT
      </div>

      <h3>
        {result.verdict === "repairable" &&
          "Likely Repairable"}

        {result.verdict === "uncertain" &&
          "Needs a Closer Look"}

        {result.verdict === "not_economical" &&
          "Repair May Not Be Worth It"}

        {result.verdict === "error" &&
          "Something Went Wrong"}
      </h3>

      <p>{result.reason}</p>

      {result.difficulty && (
        <div className="difficulty">
          <strong>Next step:</strong>{" "}
          {result.difficulty === "diy"
            ? "You may be able to handle this yourself."
            : "We recommend getting help from a professional."}
        </div>
      )}

      {result.repair_guide && (
        <div className="repair-guide">
          <strong>What you can do:</strong>
          <p>{result.repair_guide}</p>
        </div>
      )}

      {result.verdict === "not_economical" && (
       <button
  className="center-button"
  onClick={findEwasteCenter}
  disabled={centerLoading}
>
  {centerLoading
    ? "Finding a nearby center..."
    : "Find an e-waste center →"}
</button>

      )}
      {center && !center.error && (
  <div className="center-result">

    <div className="center-result-icon">♻️</div>

    <div>
      <div className="result-label">
        NEAREST SUITABLE CENTER
      </div>

      <h4>{center.name}</h4>

      <p>{center.address}</p>

      <div className="center-details">
        <span>📍 {center.distance_km} km away</span>
        <span>🕒 {center.operating_info}</span>
      </div>

      <div className="accepted">
        <strong>Accepts:</strong>{" "}
        {center.accepted_categories.join(", ")}
      </div>
      <div className="map-wrapper">
  <RepairMap center={center} />
</div>
    </div>
        
  </div>
)}

{center && center.error && (
  <div className="center-error">
    ⚠️ {center.error}
  </div>
)}

    </div>
  </div>
)}

            <div className="card-mascot">

              <div className="mini-device">
                <div className="mini-face">
                  <span>•</span>
                  <span>•</span>
                  <b>⌣</b>
                </div>
              </div>

              <div className="speech">
                <strong>Hey!</strong>

                <p>
                  I'll help you figure out what to do with your device.
                </p>
              </div>

            </div>

          </div>
        </section>

        {/* HOW IT WORKS */}
        <section
          className="how-section"
          id="how"
        >
          <div className="section-tag">
            02 / HOW IT WORKS
          </div>

          <h2>
            From broken
            <br />
            <span>to responsible.</span>
          </h2>

          <div className="steps">

            <div className="step">
              <div className="step-number">01</div>
              <div className="step-icon">🔍</div>

              <h3>Describe</h3>

              <p>
                Tell EcoRepair what device you have
                and what's going wrong.
              </p>
            </div>

            <div className="step">
              <div className="step-number">02</div>
              <div className="step-icon">🧠</div>

              <h3>Get advice</h3>

              <p>
                Our AI compares your problem
                with known repair patterns.
              </p>
            </div>

            <div className="step">
              <div className="step-number">03</div>
              <div className="step-icon">♻️</div>

              <h3>Take action</h3>

              <p>
                Repair it when practical, or find
                a suitable e-waste center.
              </p>
            </div>

          </div>
        </section>

        {/* IMPACT */}
        <section
          className="impact-section"
          id="impact"
        >

          <div className="impact-character">
            <div className="tiny-device">
              <div className="tiny-face">
                ◡ ◡
              </div>
            </div>
          </div>

          <div>
            <div className="section-tag">
              03 / WHY IT MATTERS
            </div>

            <h2>
              Every repair
              <br />
              keeps waste <span>away.</span>
            </h2>

            <p>
              Electronics don't always need to be replaced
              when something stops working. EcoRepair encourages
              informed repair decisions and responsible e-waste disposal.
            </p>
          </div>

        </section>
      </main>

      {/* FOOTER */}
      <footer>

        <div className="logo">
          <div className="logo-icon">♻</div>
          <span>EcoRepair</span>
        </div>

        <p>
          Repair more. Waste less.
        </p>

      </footer>

    </div>
  );
}

export default App;

