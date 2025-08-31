import { version } from "../version";

describe("version", () => {
  it("should return the correct version from package.json", () => {
    expect(version).toBe("0.1.0");
  });
});
