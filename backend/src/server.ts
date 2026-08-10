import "dotenv/config";

import app from "./app.js";

const PORT = Number(process.env.PORT ?? 4000);

app.listen(PORT, () => {
  console.log(
    `Academic Co-Pilot API running on http://localhost:${PORT}`,
  );
});