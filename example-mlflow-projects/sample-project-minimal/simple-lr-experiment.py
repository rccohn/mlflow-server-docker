import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import mlflow
from plotly import graph_objects as go


def get_sample_data(seed=42):
        
    xcoords = np.linspace(0, 20, 50)
    
    rng = np.random.default_rng(seed)
    noise = (rng.random(size=(xcoords.shape))-0.5)*2
    
    ycoords = 2*xcoords+3+noise

    return xcoords[:, np.newaxis], ycoords


def main():
    mlflow.set_tags({'mlflow.runName': 'linear regression test', 
    'description':'basic example of mlflow functionality'})

    x, y = get_sample_data()

    lr = LinearRegression()
    reg = lr.fit(x, y)
    r2 = lr.score(x, y)
    yp = lr.predict(x)
    mse = mean_squared_error(y,yp)

    mlflow.log_params(
                {   'slope': reg.coef_[0],
                    'intercept': reg.intercept_,
            }
    )
    
    mlflow.log_metrics(
        {
        'r-squared': r2,
        'mse': mse
    }
    )

    mlflow.sklearn.log_model(lr, 'model')

    # plot results
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        name='data',
        mode='markers',
        x=x[:, 0],
        y=y
        ))
    fig.add_trace(go.Scatter(
        name='fit',
        mode='lines',
        x=x[:, 0],
        y=yp))

    fig.write_html('results.html')
    mlflow.log_artifact('results.html')


if __name__ == "__main__":
    main()
        
