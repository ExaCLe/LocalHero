import {test, expect} from "@playwright/test";

test("shows backend health on the homepage", async ({page}) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", {name: "Backend Health"}),
  ).toBeVisible();

  await expect(page.getByText("Healthy")).toBeVisible();
});
