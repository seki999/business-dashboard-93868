import { test, expect } from "@playwright/test";

const shots = [
  ["/", "screenshots/01-dashboard.png"],
  ["/deliveries", "screenshots/02-deliveries.png"],
  ["/feedbacks", "screenshots/03-detail.png"],
  ["/batch", "screenshots/04-batch-result.png"],
  ["/logs", "screenshots/05-logs.png"],
] as const;

for (const [path, fileName] of shots) {
  test(`capture ${fileName}`, async ({ page }) => {
    await page.goto(path);
    await expect(page.locator("body")).toBeVisible();
    await page.screenshot({ path: fileName, fullPage: true });
  });
}
