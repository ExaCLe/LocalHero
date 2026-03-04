import {test, expect} from "@playwright/test";

test("shows backend health on the homepage", async ({page}) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", {name: "Backend Health"}),
  ).toBeVisible();

  await expect(
    page.getByText(/Healthy|Cannot reach Convex backend/i),
  ).toBeVisible();
  await expect(page.getByRole("link", {name: "Login"})).toBeVisible();
  await expect(page.getByRole("link", {name: "Register"})).toBeVisible();
});
