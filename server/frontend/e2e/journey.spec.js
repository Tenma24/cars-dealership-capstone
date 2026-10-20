import { test, expect } from "@playwright/test";
import fs from "node:fs";
import path from "node:path";
const evidence = path.resolve("../../evidence");
test("visitor registers, filters dealers, submits review, and logs out", async ({
  page,
}) => {
  await page.goto("/dealers");
  await expect(
    page.getByRole("link", { name: "View reviews ↗" }).first(),
  ).toBeVisible();
  await expect(
    page.getByRole("link", { name: "Review Dealer", exact: true }),
  ).toHaveCount(0);
  await page.setViewportSize({ width: 1440, height: 1800 });
  await page.screenshot({ path: path.join(evidence, "get_dealers.png") });
  await page.setViewportSize({ width: 1440, height: 1000 });
  await page.goto("/register");
  const username = "driver_" + Date.now();
  for (const [label, value] of [
    ["Username", username],
    ["First Name", "Alex"],
    ["Last Name", "Morgan"],
    ["Email", "alex@example.com"],
    ["Password", "RoadJourney!72zQ"],
  ])
    await page.getByLabel(label, { exact: true }).fill(value);
  await page.getByRole("button", { name: "Register", exact: true }).click();
  await expect(page.locator(".username")).toHaveText(username);
  await expect(
    page.getByRole("link", { name: "Review Dealer", exact: true }).first(),
  ).toBeVisible();
  await page.screenshot({
    path: path.join(evidence, "get_dealers_loggedin.png"),
  });
  await page.getByLabel("Filter by state").selectOption("Kansas");
  await expect(page).toHaveURL(/state=Kansas/);
  await expect(page.locator("tbody tr").first()).toContainText("Kansas");
  await page.screenshot({ path: path.join(evidence, "dealersbystate.png") });
  await page.getByRole("link", { name: "View reviews ↗" }).first().click();
  await expect(
    page.getByRole("heading", { name: "Customer experiences" }),
  ).toBeVisible();
  await page.screenshot({ path: path.join(evidence, "dealer_id_reviews.png") });
  await page.getByRole("link", { name: "Review Dealer ↗" }).click();
  const review =
    "Fantastic services! The team explained every option clearly and made the visit easy.";
  await page.getByLabel("Your review").fill(review);
  await page.getByLabel("I purchased a vehicle").check();
  await page.getByLabel("Car make").selectOption({ label: "Audi" });
  await page.getByLabel("Car model / year").selectOption({ index: 1 });
  await page.getByLabel("Purchase date").fill("2026-10-01");
  await page.screenshot({
    path: path.join(evidence, "dealership_review_submission.png"),
  });
  await page.getByRole("button", { name: "Post review", exact: true }).click();
  await expect(page.getByText(review, { exact: true }).last()).toBeVisible();
  await page.getByText(review, { exact: true }).last().scrollIntoViewIfNeeded();
  await page.screenshot({ path: path.join(evidence, "added_review.png") });
  await page.getByRole("button", { name: "Log out", exact: true }).click();
  await expect(
    page.getByRole("link", { name: "Log in", exact: true }),
  ).toBeVisible();
});
test("admin signs in and signs out", async ({ page }) => {
  const config = JSON.parse(fs.readFileSync("../../.local-config.json"));
  await page.goto("/admin/");
  await page.getByLabel("Username:").fill("root");
  await page.getByLabel("Password:").fill(config.ADMIN_PASSWORD);
  await page.getByRole("button", { name: "Log in", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Site administration" }),
  ).toBeVisible();
  await page.screenshot({ path: path.join(evidence, "admin_login.png") });
  await page.getByRole("button", { name: "Log out", exact: true }).click();
  await expect(page.getByRole("heading", { name: "Logged out" })).toBeVisible();
  await page.screenshot({ path: path.join(evidence, "admin_logout.png") });
});
test("mobile directory and information pages are readable", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/dealers");
  await expect(
    page.getByRole("heading", { name: "Find your next chapter." }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBeTruthy();
  await page.screenshot({ path: path.join(evidence, "mobile.png") });
  for (const [url, title] of [
    ["/about/", "About Us"],
    ["/contact/", "Contact Us"],
  ]) {
    await page.goto(url);
    await expect(page.getByRole("heading", { name: title })).toBeVisible();
  }
});
