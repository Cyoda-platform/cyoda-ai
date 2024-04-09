import com.fasterxml.jackson.databind.ObjectMapper
import io.cloudevents.core.builder.CloudEventBuilder
import io.cloudevents.core.data.PojoCloudEventData
import io.cloudevents.core.format.EventFormat
import io.cloudevents.core.provider.EventFormatProvider
import io.cloudevents.protobuf.ProtobufFormat
import io.cloudevents.v1.proto.CloudEvent
import io.github.oshai.kotlinlogging.KotlinLogging
import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder
import io.grpc.stub.StreamObserver
import org.cyoda.cloud.api.event.common.BaseEvent
import org.cyoda.cloud.api.event.common.CloudEventType
import org.cyoda.cloud.api.event.common.DataPayload
import org.cyoda.cloud.api.event.processing.CalculationMemberJoinEvent
import org.cyoda.cloud.api.event.processing.EntityProcessorCalculationRequest
import org.cyoda.cloud.api.event.processing.EntityProcessorCalculationResponse
import org.cyoda.cloud.api.grpc.CloudEventsServiceGrpc
import org.springframework.beans.factory.DisposableBean
import org.springframework.beans.factory.InitializingBean
import org.springframework.context.event.ContextRefreshedEvent
import org.springframework.context.event.EventListener
import org.springframework.stereotype.Component
import java.lang.NullPointerException
import java.net.URI
import java.util.*
import java.util.concurrent.TimeUnit

private val logger = KotlinLogging.logger {}

/**
 * This is a simple client for demonstration purposes only and should not be used in a production environment
 * as it does not do the necessary configuration for timeouts, error handling, message size config etc.
 */
@Component
class CyodaCalculationMemberClient(
    private val objectMapper: ObjectMapper,
    private val processor: CyodaCalculationMemberProcessor
) : DisposableBean, InitializingBean {

    private var managedChannel: ManagedChannel? = null
    private var clientStub: CloudEventsServiceGrpc.CloudEventsServiceStub? = null
    private var streamingObserver: StreamObserver<CloudEvent>? = null
    private val eventFormat: EventFormat = EventFormatProvider
        .getInstance()
        .resolveFormat(ProtobufFormat.PROTO_CONTENT_TYPE)
        ?: throw NullPointerException("Unable to resolve protobuf event format")

    override fun afterPropertiesSet() {
        managedChannel = ManagedChannelBuilder
            .forAddress("localhost", 50051)
            .usePlaintext()
            .build()
        clientStub = CloudEventsServiceGrpc.newStub(managedChannel)
            .withWaitForReady()
    }

    @EventListener
    fun onApplicationEvent(contextRefreshedEvent: ContextRefreshedEvent) {
        streamingObserver = clientStub!!.startStreaming(object : StreamObserver<CloudEvent> {

            override fun onNext(value: CloudEvent) {
                logger.info { ">> Got EVENT:\n$value" }
                when (value.type) {
                    CloudEventType.ENTITY_PROCESSOR_CALCULATION_REQUEST.value() -> {
                        sendEvent(
                            processor.calculate(
                                objectMapper.readValue(
                                    value.textData,
                                    EntityProcessorCalculationRequest::class.java
                                )
                            )
                        )
                    }

                    else -> logger.info { "Skipping message as no processing required" }
                }
            }

            override fun onError(t: Throwable) {
                logger.error(t) { ">> Got ERROR from remote backend" }
            }

            override fun onCompleted() {
                logger.info { ">> Got COMPLETE from remote backend" }
            }
        })

        sendEvent(CalculationMemberJoinEvent().apply {
            this.owner = "PLAY"
            this.tags = listOf("simple", "sample")
        })
    }

    fun sendEvent(event: BaseEvent) {
        val cloudEvent = CloudEvent.parseFrom(
            eventFormat.serialize(
                CloudEventBuilder.v1()
                    .withType(event.javaClass.simpleName)
                    .withSource(URI.create("SimpleSample"))
                    .withId(UUID.randomUUID().toString())
                    .withData(PojoCloudEventData.wrap(event) { objectMapper.writeValueAsBytes(it) })
                    .build()
            )
        )

        val observer = streamingObserver

        check(observer != null) {
            "Stream observer is not initialized"
        }

        logger.info { "<< Sending EVENT:\n$event" }
        // stream observer is not thread safe, for production usage this should be managed by some pooling for such cases
        synchronized(observer) {
            observer.onNext(cloudEvent)
        }
    }

    override fun destroy() {
        streamingObserver?.onCompleted()
        managedChannel?.shutdown()
            ?.awaitTermination(10, TimeUnit.SECONDS)
    }

}

@Component
class CyodaCalculationMemberProcessor {

    fun calculate(request: EntityProcessorCalculationRequest): BaseEvent {



        return EntityProcessorCalculationResponse().apply {
            owner = request.owner
            requestId = request.requestId
            entityId = request.entityId
            payload = DataPayload().apply {
                type = "TreeNode"
                data = request.payload?.data
            }
        }
    }

}