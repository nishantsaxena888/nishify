import { fetchEntityData } from "../api";
import { USE_MOCK } from "../config";

// Required to reset mock state
jest.resetModules();

describe("fetchEntityData - mock mode", () => {
  beforeEach(() => {
    jest.resetModules(); // Clear module cache to re-import fresh mock
  });

  it("should return options from mock", async () => {
    const res = await fetchEntityData("products", "options");
    expect(res.fields).toBeDefined();
    expect(res.fields.length).toBeGreaterThan(0);
  });

  it("should return list of products", async () => {
    const res = await fetchEntityData("products", "get");
    expect(Array.isArray(res)).toBe(true);
    expect(res.length).toBeGreaterThan(0);
  });

  it("should return a single product by ID", async () => {
    const product = await fetchEntityData("products", "getOne", { id: "p2" });
    expect(product).toBeDefined();
    expect(product.id).toBe("p2");
  });

  it("should add a new product", async () => {
    const newProduct = await fetchEntityData("products", "post", {
      name: "Tablet",
      price: 400,
    });

    expect(newProduct.id).toMatch(/id-/);
    expect(newProduct.name).toBe("Tablet");

    const updatedList = await fetchEntityData("products", "get");
    expect(updatedList.find((p) => p.id === newProduct.id)).toBeTruthy();
  });

  it("should update an existing product", async () => {
    const updated = await fetchEntityData("products", "update", {
      id: "p2",
      name: "Phone Ultra",
      price: 899,
    });

    expect(updated.name).toBe("Phone Ultra");
    expect(updated.price).toBe(899);
  });

  it("should fail if mock handler not implemented", async () => {
    await expect(fetchEntityData("products", "delete" as any)).rejects.toThrow(
      "Mock not implemented for products delete"
    );
  });
});
