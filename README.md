# sigma
Data Science for Life Sciences - Semester 1 project

## Content:
1) Creating a virtual environment
2) Running the dashboard.
3) Adding your own components.

## 1) Creating a virtual environment
Go to your editor and create a new virtual environment.

Activate the environment and use the following command:

`pip install -r requirements.txt`

## 1) Running the dashboard
Make sure you have an original copy of the dashboard. Otherwise, clone it to your local system with:
`git clone https://github.com/PRiesebos/sigma.git`

To run the dashboard:
```
cd main
python3 main.py
```

## 2) Creating your own pages
To create your own page, it requires you to put your figure into a `panel pane`. 

For examples, look into the `pages` folder location in `main/dashboard/pages/`. This folder contains several pages you 
can look into as example, but do not modify them.

The flow of the app works as follows:
```
main.py is used to boot the dashboard and add all the panes.
dashboard.py contains the dashboard itself.
pages/ contain the pages that are added to the dashboard class in main.py
```

A page requires the following format:
```python
class MyPage:
    def __init__(self):
        self.pane = my_pane # populate this with a panels pane.
        self.button = my_button # populate this with a button.
    def get_contents(self):
        return self.pane, self.button
```

This class will be imported in `main.py` in the following way:
```python
from dashboard.pages import MyPage

my_page = MyPage()
my_pane, my_btn = about_page.get_contents()

# make sure the same identifier is used for the pane and the 
# button for navigation purposes.
panes = {
    'my_page': my_pane
}
btns = {
    'my_page': my_btn,
}

if __name__ == '__main__':
    dashboard = Dashboard(title='SIGMA', panes=panes, btns=btns, home_pane='paper')
    dashboard.serve(50000)
```
Last but not least, don't forget to register your identifier in the Dashboard callback:
If you want the button to do something else, you can make a custom callback in the `get_callback` function.

```python
    def get_callback(self, key):
        """Callbacks that can alter the dashboard."""

        def change_pane(event):
            self.row[0] = self.panes[key]

        collection = {
            'paper': change_pane,
            'about': change_pane,
            'biome': change_pane,
            'spo2': change_pane,
            'my_page': change_pane # <- register here
        }

        return collection[key]
```

So, if you follow the flow of the code, it would soon become even more clear and very easy to implement your own page!