class MockResponse:
  def __init__(self, responseJson):
    def json():
      return responseJson

    self.json = json
