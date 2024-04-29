class HttpEndpointDto {
    
    private String operation;
    //description of the operation
    private String type;
    private String query;
    private HttpEndpoint.Method method;
    private List<HttpParameterDto> parameters = new ArrayList<>();
    private String bodyTemplate;
    private Integer connectionTimeout;
    private Integer readWriteTimeout;

    public enum Method {
        GET,
        POST_BODY   // putting content(for example JSON) as post body
    }
} 

 class HttpParameterDto  {
    private String name;
    private String defaultValue;
    private boolean secure;
    private boolean required;
    //if is calculated via velocity function, default = false
    private boolean template;
    //velocity function for a template
    private String templateValue;
    //if parameter should be excluded from the cache key - is false by default
    private boolean excludeFromCacheKey;
    private HttpParameterDto.ParameterType type;
    //just pass emty list
    private List<String> optionValues;

    enum ParameterType {
        PATH_VARIABLE, //for example GET http://host.com/{parameter}
        REQUEST_BODY_VARIABLE,//for POST request body
        REQUEST_PARAM, //for example GET http://host.com?parameter=x
        HEADER_PARAM, //header
        TEMPLATE_VARIABLE, //velocity function parameter
        CUSTOM_PARAM //util parameter

    }
}