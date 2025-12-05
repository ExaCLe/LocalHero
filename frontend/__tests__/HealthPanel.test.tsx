import {render, screen} from "@testing-library/react";
import {HealthPanel, HealthResponse} from "../components/HealthPanel";

describe("HealthPanel", () => {
  test("shows unreachable message when health is null", () => {
    render(<HealthPanel health={null}/>);

    expect(
      screen.getByText(/Cannot reach backend/i),
    ).toBeInTheDocument();
  });

  test("shows healthy state when status and DB are ok", () => {
    const health: HealthResponse = {
      status: "ok",
      database: "connected",
    };

    render(<HealthPanel health={health}/>);

    expect(screen.getByText(/✅ Healthy/i)).toBeInTheDocument();
    expect(screen.getByText(/Status:/i)).toHaveTextContent(
      "Status: ok, DB: connected",
    );
  });

  test("shows unhealthy state when status or DB differ", () => {
    const health: HealthResponse = {
      status: "error",
      database: "disconnected",
    };

    render(<HealthPanel health={health}/>);

    expect(screen.getByText(/⚠️ Unhealthy/i)).toBeInTheDocument();
    expect(screen.getByText(/Status:/i)).toHaveTextContent(
      "Status: error, DB: disconnected",
    );
  });
});
