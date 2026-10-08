from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <!DOCTYPE html>
    <html lang="hr">

    <head>

        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>StudyMate 🎓</title>

        <style>

            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f5f7fb;
                color: #111827;
            }

            .header {
                background: white;
                padding: 20px 35px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 10px #00000010;
            }

            .logo {
                font-size: 28px;
                font-weight: bold;
                color: #2563eb;
            }

            .container {
                max-width: 1100px;
                margin: 40px auto;
                padding: 20px;
            }

            .welcome {
                margin-bottom: 30px;
            }

            .welcome h1 {
                font-size: 36px;
                margin-bottom: 8px;
            }

            .welcome p {
                color: #6b7280;
                font-size: 18px;
            }

            .grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
            }

            .card {
                background: white;
                border-radius: 18px;
                padding: 30px;
                min-height: 180px;
                box-shadow: 0 5px 20px #00000010;
                cursor: pointer;
                transition: 0.2s;
            }

            .card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px #00000018;
            }

            .icon {
                font-size: 42px;
                margin-bottom: 15px;
            }

            .card h2 {
                margin: 0 0 10px;
                font-size: 22px;
            }

            .card p {
                color: #6b7280;
                margin: 0;
                line-height: 1.5;
            }

            @media (max-width: 800px) {

                .grid {
                    grid-template-columns: repeat(2, 1fr);
                }

            }

            @media (max-width: 550px) {

                .grid {
                    grid-template-columns: 1fr;
                }

                .header {
                    padding: 18px;
                }

                .container {
                    margin: 20px auto;
                }

            }

        </style>

    </head>


    <body>

        <header class="header">

            <div class="logo">
                🎓 StudyMate
            </div>

            <div>
                🌍 Hrvatski
            </div>

        </header>


        <main class="container">

            <div class="welcome">

                <h1>Dobrodošao u StudyMate 👋</h1>

                <p>
                    Sve što ti treba za lakše i pametnije učenje.
                </p>

            </div>


            <div class="grid">


                <div class="card" onclick="openFeature('ai')">

                    <div class="icon">
                        🤖
                    </div>

                    <h2>AI pomoćnik</h2>

                    <p>
                        Postavi pitanje i pomozi si uz AI.
                    </p>

                </div>


                <div class="card" onclick="openFeature('history')">

                    <div class="icon">
                        🕘
                    </div>

                    <h2>Povijest</h2>

                    <p>
                        Pregledaj svoja prethodna pitanja i razgovore.
                    </p>

                </div>


                <div class="card" onclick="openFeature('quiz')">

                    <div class="icon">
                        📝
                    </div>

                    <h2>Kvizovi</h2>

                    <p>
                        Testiraj svoje znanje kroz različite kvizove.
                    </p>

                </div>


                <div class="card" onclick="openFeature('calculator')">

                    <div class="icon">
                        🧮
                    </div>

                    <h2>Kalkulator</h2>

                    <p>
                        Rješavaj matematičke zadatke i računaj.
                    </p>

                </div>


                <div class="card" onclick="openFeature('materials')">

                    <div class="icon">
                        📚
                    </div>

                    <h2>Materijali</h2>

                    <p>
                        Organiziraj i koristi svoje materijale za učenje.
                    </p>

                </div>


                <div class="card" onclick="openFeature('settings')">

                    <div class="icon">
                        ⚙️
                    </div>

                    <h2>Postavke</h2>

                    <p>
                        Jezik, izgled i ostale postavke StudyMatea.
                    </p>

                </div>


            </div>

        </main>


        <script>

            function openFeature(feature) {

                if (feature === "ai") {
                    alert("AI pomoćnik – uskoro!");
                }

                else if (feature === "history") {
                    alert("Povijest – uskoro!");
                }

                else if (feature === "quiz") {
                    alert("Kvizovi – uskoro!");
                }

                else if (feature === "calculator") {
                    alert("Kalkulator – uskoro!");
                }

                else if (feature === "materials") {
                    alert("Materijali – uskoro!");
                }

                else if (feature === "settings") {
                    alert("Postavke – uskoro!");
                }

            }

        </script>

    </body>

    </html>
    """